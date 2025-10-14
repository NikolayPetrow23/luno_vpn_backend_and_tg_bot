import datetime
from jose import JWTError, jwt

from src.models.user import User
from src.dao.subscribtion import PlanSubscriptionDAO
from src.dao.payment import PaymentDAO
from src.exceptions import (
    IncorrectEmailOrPasswordException,
    IncorrectTokenException, 
    TokenExpiredException,
    UserAlreadyExistsException,
    UserIsNotPresentException
)
from src.schemas.auth import TokenResponse
from src.config import settings
from src.utils.jwt_handler import create_access_token
from src.utils.payment import create_yookassa_payment


class PaymentService:
    @staticmethod
    async def process_payment(plan_id: int, user_id: int) -> None:
        plan = await PlanSubscriptionDAO.find_one_or_none(id=plan_id)
        last_payment = await PaymentDAO.find_last()
        payment = await create_yookassa_payment(
            amount=plan.price,
            description=f"Заказ # {last_payment.id + 1 if last_payment != None else 1}, подписка {plan.name}",
            user_id=user_id,
            plan_id=plan_id
        )
        return payment

    @staticmethod
    async def handle_webhook(payment_data: dict) -> None:
        # Обработка webhook от платежной системы
        # Тут мы создаем запись о платеже, привязываем подписку к пользователю и т.д.
        # Тут мы создаем 
        if payment_data.get("event") == "payment.succeeded":
            metadata = payment_data.get("object", {}).get("metadata", {})
            user_id = metadata.get("user_id")
            plan_id = metadata.get("plan_id")
            plan = await PlanSubscriptionDAO.find_one_or_none(id=plan_id)
            if plan:
                # Логика предоставления доступа пользователю к подписке
                pass


    # @staticmethod
    # async def (payment_data: dict) -> None:
    #     payment = await create_payment()
    #     ...


# {'type': 'notification', 'event': 'payment.succeeded', 'object': {'id': '30809d33-000f-5000-b000-116c5eca6683', 'status': 'succeeded', 'amount': {'value': '50.00', 'currency': 'RUB'}, 'income_amount': {'value': '48.25', 'currency': 'RUB'}, 'description': 'Заказ 1, подписка 1 месяц', 'recipient': {'account_id': '1186099', 'gateway_id': '2558064'}, 'payment_method': {'type': 'yoo_money', 'id': '30809d33-000f-5000-b000-116c5eca6683', 'saved': False, 'status': 'inactive', 'title': 'YooMoney wallet 410011758831136', 'account_number': '410011758831136'}, 'captured_at': '2025-10-14T17:34:15.477Z', 'created_at': '2025-10-14T17:33:39.285Z', 'test': True, 'refunded_amount': {'value': '0.00', 'currency': 'RUB'}, 'paid': True, 'refundable': True, 'metadata': {'user_id': '3', 'cms_name': 'yookassa_sdk_python', 'plan_id': '1'}}}