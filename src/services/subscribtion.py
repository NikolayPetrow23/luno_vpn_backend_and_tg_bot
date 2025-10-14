import datetime
from jose import JWTError, jwt

from src.dao.subscribtion import PlanSubscriptionDAO
from src.models.subscription import PlanSubscription
from src.dao.user import UserDAO

from src.schemas.subscription import SPlanSubscription


class SubscriptionService:
    @staticmethod
    async def create_subscription(payment_data: dict) -> None:
        payment = await create_payment()
        ...

    @staticmethod
    async def plan_subscription() -> SPlanSubscription:
        plans = await PlanSubscriptionDAO.find_all()
        return [SPlanSubscription.model_validate(plan) for plan in plans]
    