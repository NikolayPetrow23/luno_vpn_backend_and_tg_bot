import datetime
import json

from src.exceptions import (
    ExceptionInCreatingPayment, 
    PlanNotFound, 
    PaymentTypeNotFound,
    PaymentIsAlreadyConfirmed
)
from src.models.enum import PaymentStatus
from src.models import User, Payment, PlanSubscription, Subscription, Server, ShortLink, PaymentType
from src.dao.subscribtion import PlanSubscriptionDAO, SubscriptionDAO
from src.dao.payment import PaymentDAO, PaymentTypeDAO
from src.dao.user import UserDAO
from src.dao.short_link import ShortLinkDAO
from src.dao.server import ServerDAO
from src.utils.payment import create_payment_platega
from src.utils.utils import utc_now_no_microseconds
from src.services.vpn_client import VpnServerClient
from src.broker.nats import nats
from src.broker.admin import push_exception_admin


class PaymentService:
    @staticmethod
    async def process_payment_platega(plan_id: int, payment_method: int, user_id: int) -> None:
        try:
            plan = await PlanSubscriptionDAO.find_one_or_none(id=plan_id)
        except Exception as e:
            await push_exception_admin(
                user_id=user_id,
                exception=e,
                path="PaymentService.process_payment_platega",
                raise_exc="PlanNotFound - План подписки не найден!"
            )
            raise PlanNotFound.set_detail(
                f"План подписки не найден!"
            )
        
        last_payment: Payment | None = await PaymentDAO.find_last()
        payment_method: PaymentType | None = await PaymentTypeDAO.find_one_or_none(code=payment_method)

        if payment_method is None:
            await push_exception_admin(
                user_id=user_id,
                exception=None,
                path="PaymentService.process_payment_platega",
                raise_exc="PaymentTypeNotFound - Метод оплаты не найден!"
            )
            raise PaymentTypeNotFound.set_detail(
                f"Метод оплаты не найден!"
            )
        
        try:
            payment = await create_payment_platega(
                payment_method=payment_method.code,
                amount=plan.price,
                description=f"Заказ # {last_payment.id + 1 if last_payment != None else 1}, подписка {plan.name}",
                user_id=user_id,
                plan_id=plan_id
            )
        except Exception as e:
            await push_exception_admin(
                user_id=user_id,
                exception=e,
                path="PaymentService.process_payment_platega",
                raise_exc="ExceptionInCreatingPayment - Произошла ошибка при создании платежа!"
            )
            raise ExceptionInCreatingPayment.set_detail(
                f"Произошла ошибка при создании платежа!"
            )
        
        if not payment or payment.get("status") != PaymentStatus.PENDING.value:
            raise "Платеж не создан, произошла какая-то ошибка!"
        
        try:
            await PaymentDAO.add_data(
                user_id=user_id,
                payment_type_id=payment_method.id,
                plan_id=plan.id,
                transaction_id=payment["transactionId"],
                amount=float(plan.price),
                income_amount=float(
                    float(plan.price) - 
                    (float(plan.price) * payment_method.commission_percentage)
                ),
                currency=payment["paymentDetails"].split(" ")[1],
                status=PaymentStatus.PENDING
            )
        except Exception as e:
            await push_exception_admin(
                user_id=user_id,
                exception=e,
                path="PaymentService.process_payment_platega",
                raise_exc="ExceptionInCreatingPayment - Произошла ошибка при создании платежа в базе данных!"
            )
            raise ExceptionInCreatingPayment.set_detail(
                f"Произошла ошибка при создании платежа в базе данных!"
            )
        
        return {
            "payment_link": payment.get("redirect"),
            "plan": plan,
            "order_id": last_payment.id + 1 if last_payment != None else 1
        }


    @classmethod
    async def handle_webhook_platega(
        cls, 
        transaction_id: str, 
        status: str
    ) -> dict:
        try:
            payment: Payment = await PaymentDAO.find_one_or_none(
                transaction_id=transaction_id
            )
            if not payment:
                raise Exception("Не найден платеж бля!")
            
            user: User = await UserDAO.find_one_or_none(
                id=payment.user_id
            )
            plan: PlanSubscription = await PlanSubscriptionDAO.find_one_or_none(
                id=payment.plan_id
            )
            if not user or not plan:
                raise Exception("Не найден пользователь или платеж!")
            
            if status == PaymentStatus.CONFIRMED.value:
                if payment.status == PaymentStatus.CONFIRMED:
                    raise PaymentIsAlreadyConfirmed.set_detail(
                        f"Платеж с transaction_id {transaction_id} уже подтвержден!"
                    )
                servers = await ServerDAO.find_servers_is_active_in_domain()
                subscription_id = await cls._handle_confirmed(
                    payment, 
                    user,
                    plan, 
                    servers
                )
                return {"subscription_id": subscription_id}
            
            elif status == PaymentStatus.EXPIRED.value:
                await PaymentDAO.update_data(
                    model_id=payment.id, 
                    status=PaymentStatus.EXPIRED
                )
                await PaymentService._notify_user(
                    user, 
                    plan, 
                    "client.payment.expired"
                )
                return {"status": "expired"} 
            elif status == PaymentStatus.CANCELED.value:
                await PaymentDAO.update_data(
                    model_id=payment.id,
                    status=PaymentStatus.CANCELED
                )
                await PaymentService._notify_user(
                    user, 
                    plan, 
                    "client.payment.cancaled"
                )
            else:
                await PaymentDAO.update_data(
                    model_id=payment.id,
                    status=PaymentStatus.NONE
                )
                await cls._notify_user(
                    user, 
                    plan, 
                    "client.payment.other_status"
                )
                await push_exception_admin(
                    user_id=user.id,
                    exception=None,
                    path="PaymentService.handle_webhook_platega",
                    raise_exc="Получен неизвестный статус платежа из вебхука!"
                )
        except Exception as e:
            await push_exception_admin(
                user_id=user.id,
                exception=e,
                path="PaymentService.handle_webhook_platega",
                raise_exc="Exception - Произошла ошибка при обработке вебхука платежа!"
            )
            raise Exception
    
    @classmethod
    async def _handle_confirmed(
        cls, 
        payment: Payment, 
        user: User,
        plan: PlanSubscription, 
        servers: Server
    ):
        active_sub: Subscription | None = await SubscriptionDAO.find_one_or_none(
            user_id=user.id, 
            is_active=True
        )

        if active_sub:
            await SubscriptionDAO.update_data(
                model_id=active_sub.id, 
                is_active=False
            )
            end_date: datetime = active_sub.end_date + datetime.timedelta(
                days=plan.duration_days
            )
            subscription: Subscription = await SubscriptionDAO.add_data(
                user_id=user.id,
                plan_id=plan.id,
                end_date=end_date,
                is_active=True
            )
            short_link: ShortLink = await ShortLinkDAO.find_one_or_none(
                subscription_id=active_sub.id
            )
            await ShortLinkDAO.update_data(
                model_id=short_link.id,
                subscription_id=subscription.id
            )
            await VpnServerClient.remove_user_to_all_servers(
                servers=servers,
                uuid=active_sub.uuid,
                email=f"tg_{user.telegram_id}"
            )
            await PaymentService._notify_user(
                user=user, 
                plan=plan, 
                payload_type="client.payment.update_subscription",
                end_date=end_date
            )
        else:
            end_date: datetime = utc_now_no_microseconds() + datetime.timedelta(
                days=plan.duration_days
            )
            subscription: Subscription = await SubscriptionDAO.add_data(
                user_id=user.id,
                plan_id=plan.id,
                end_date=end_date,
                is_active=True
            )
            await ShortLinkDAO.add_data(
                subscription_id=subscription.id
            )
            await PaymentService._notify_user(
                user=user, 
                plan=plan, 
                payload_type="client.payment.new_subscription",
                end_date=end_date
            )
        
        await VpnServerClient.add_user_to_all_servers(
            servers=servers,
            uuid=subscription.uuid,
            email=f"tg_{user.telegram_id}"
        )

        await PaymentDAO.update_data(
            model_id=payment.id,
            subscription_id=subscription.id,
            status=PaymentStatus.CONFIRMED
        )
        return subscription.id

    @classmethod
    async def _notify_user(
        cls, 
        user,
        plan, 
        payload_type, 
        end_date=None
    ):
        payload = {
            "type": payload_type,
            "user_id": user.telegram_id,
            "plan_name": plan.name,
            "count_devices": plan.count_devices,
            "end_date": end_date.strftime("%d.%m.%Y") if end_date else None,
            "price": plan.price,
        }
        await nats.publish(
            "bot.client.notifications", 
            json.dumps(payload).encode()
        )