import datetime
import json

from src.exceptions import SubscriptionActiveException, PlanNotFound, ShortLinkNotFound
from src.dao.configuration import ConfigurationDAO
from src.dao.user import UserDAO
from src.models import Subscription, ShortLink, PlanSubscription, User
from src.dao.subscribtion import PlanSubscriptionDAO, RefferalDAO, SubscriptionDAO
from src.dao.short_link import ShortLinkDAO
from src.schemas.subscription import SPlanSubscription, SXrayClient, SXrayClients
from src.schemas.user import SUser
from src.utils.utils import utc_now_no_microseconds
from src.broker.nats import nats
from src.broker.admin import push_exception_admin


class SubscriptionService:
    @staticmethod
    async def subsription_plan_user(user_id: int):
        try:
            sub = await SubscriptionDAO.find_subscription_active_in_user(user_id=user_id)
            return sub
        except Exception as e:
            await push_exception_admin(
                user_id=user_id,
                exception=e,
                path="SubscriptionService.subsription_plan_user",
                raise_exc=f"Произошла ошибка поиска активной подписки для юзера - {user_id}"
            )
            raise
        
    @staticmethod
    async def get_short_link(user_id: int) -> ShortLink:
        try:
            sub: Subscription | None = await SubscriptionDAO.find_short_link(user_id=user_id)
            short_link: ShortLink |  None = sub.short_link.code
            if not short_link:
                raise ShortLinkNotFound.set_detail("Short link не найден!")
            return short_link
        except ShortLinkNotFound as e:
            await push_exception_admin(
                user_id=user_id,
                exception=e,
                path="SubscriptionService.get_short_link",
                raise_exc=f"Short link не найден для user_id={user_id}"
            )
            raise
        except Exception as e:
            await push_exception_admin(
                user_id=user_id,
                exception=e,
                path="SubscriptionService.get_short_link",
                raise_exc=f"Произошла ошибка поиска short_link для юзера - {user_id}"
            )
            raise

    @staticmethod
    async def plan_subscription() -> list[SPlanSubscription]:
        plans = await PlanSubscriptionDAO.find_all()
        if not plans:
            await push_exception_admin(
                user_id=None,
                exception=None,
                path="SubscriptionService.plan_subscription",
                raise_exc=f"PlanNotFound - Планы подписок не найдены!"
            )
            raise PlanNotFound.set_detail("Планы подписок не найдены!")
        return [SPlanSubscription.model_validate(plan) for plan in plans]
        
    @classmethod
    async def subsribtion_is_active_all(cls) -> SXrayClients:
        subs = await SubscriptionDAO.find_all_is_active_subscription()
        users = [SXrayClient.model_validate({
            "id": sub.uuid,
            "email": f"tg_{sub.user.telegram_id}"
        }) for sub in subs]
        return SXrayClients(users=users)

    @classmethod
    async def check_expired_subscriptions(cls) -> SXrayClients:
        try:
            now = utc_now_no_microseconds()
            users_lst_expired: list = await SubscriptionDAO.update_expire_subsrciption(now=now)
            payload = {
                "type": "client.subscription.expired.notify",
                "users_lst_expired": users_lst_expired
            }
            await nats.publish("bot.client.notifications", json.dumps(payload).encode())
            users_lst_expire: list = await SubscriptionDAO.check_expire_subsrciption(day=1)
            payload = {
                "type": "client.subscription.expire.notify",
                "users_lst_expire": users_lst_expire
            }
            await nats.publish("bot.client.notifications", json.dumps(payload).encode())
            return await cls.subsribtion_is_active_all()
        except Exception as e:
            await push_exception_admin(
                user_id=None,
                exception=e,
                path="SubscriptionService.check_expired_subscriptions",
                raise_exc=f"SubscriptionActiveException - Не удалось проверить истекшие подписки!"
            )
            raise SubscriptionActiveException.set_detail(f"Не удалось проверить истекшие подписки!")
        
    @classmethod    
    async def activate_testing_subscribe(cls, user_id: int):
        user: User = await UserDAO.find_one_or_none(id=user_id)
        if user.is_testing_subscribe:
            raise SubscriptionActiveException.set_detail("Пробная подписка уже активированна!")

        plan_free = await PlanSubscriptionDAO.find_one_or_none(
            name="Пробная подписка"
        )

        if not plan_free:
            raise PlanNotFound.set_detail("Пробный план не найден")

        try:
            await UserDAO.update_data(model_id=user.id, is_testing_subscribe=True)
            end_date = utc_now_no_microseconds() + datetime.timedelta(days=plan_free.duration_days)
            subscription = await SubscriptionDAO.add_data(
                user_id=user.id,
                plan_id=plan_free.id,
                end_date=end_date,
                is_active=True
            )
            await ShortLinkDAO.add_data(
                subscription_id=subscription.id
            )
        except Exception as e:
            raise SubscriptionActiveException.set_detail(f"Не удалось активировать пробный период: {e}")

        return subscription


class RefferalService:
    @staticmethod
    async def process_refferal(user_data: SUser, ref_code: str):
        referee: User | None  = await UserDAO.find_one_or_none(
            telegram_id=user_data.telegram_id
        )
        
        if referee is None:
            referee = await UserDAO.add_data(
                telegram_id=user_data.telegram_id,
                username=user_data.username,
                first_name=user_data.first_name
            )
            referrer: User | None = await UserDAO.find_one_or_none(ref_code=ref_code)          
            sub_referrer: Subscription | None = await SubscriptionDAO.find_one_or_none(
                user_id=referrer.id, is_active=True
            )
            configuration = await ConfigurationDAO.find_config()
            reward_ref = configuration.reward_ref
            plan_free: PlanSubscription | None = await PlanSubscriptionDAO.find_one_or_none(
                name="Пробная подписка"
            )

            if sub_referrer is None:
                referrer_subscription = await SubscriptionDAO.add_data(
                    user_id=referrer.id,
                    plan_id=plan_free.id,
                    end_date=utc_now_no_microseconds() + datetime.timedelta(
                        days=plan_free.duration_days
                    ),
                    is_active=True
                )
                await ShortLinkDAO.add_data(
                    subscription_id=referrer_subscription.id
                )
                payload = {
                    "type": "client.refferer.new_subscription",
                    "user_id": referrer.telegram_id,
                    "reward_ref": reward_ref
                }   
                await nats.publish("bot.client.notifications", json.dumps(payload).encode())
            else:
                await SubscriptionDAO.update_data(
                    model_id=sub_referrer.id, 
                    end_date=sub_referrer.end_date+datetime.timedelta(days=reward_ref)
                )
                payload = {
                    "type": "client.refferer.update_subscription",
                    "user_id": referrer.telegram_id,
                    "reward_ref": reward_ref
                }   
                await nats.publish("bot.client.notifications", json.dumps(payload).encode())

            referee_subscription = await SubscriptionDAO.add_data(
                user_id=referee.id,
                plan_id=plan_free.id,
                end_date=utc_now_no_microseconds() + datetime.timedelta(
                    days=plan_free.duration_days + reward_ref
                ),
                is_active=True
            )

            await ShortLinkDAO.add_data(
                subscription_id=referee_subscription.id
            )

            await RefferalDAO.add_data(
                referrer_id=referrer.id,
                referee_id=referee.id,
                ref_code=ref_code
            )

            payload = {
                "type": "client.referee.new_subscription",
                "user_id": referee.telegram_id,
                "reward_ref": reward_ref
            }   
            await nats.publish("bot.client.notifications", json.dumps(payload).encode())
