from sqlalchemy import insert, select
from src.dao.base import BaseDAO
from src.models import Subscription, PlanSubscription

from src.database import async_session_maker


class SubscriptionDAO(BaseDAO):
    model = Subscription


class PlanSubscriptionDAO(BaseDAO):
    model = PlanSubscription
