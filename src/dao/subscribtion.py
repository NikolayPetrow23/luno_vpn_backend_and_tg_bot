from datetime import datetime
from sqlalchemy import Date, func, select, update, cast
from sqlalchemy.orm import joinedload
from src.dao.base import BaseDAO
from src.models import Subscription, PlanSubscription, Referral, User

from src.database import async_session_maker


class SubscriptionDAO(BaseDAO):
    model = Subscription

    @classmethod
    async def find_subscription_active_in_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(
                cls.model
            ).where(
                cls.model.user_id == user_id,
                cls.model.is_active == True
            ).options(
                joinedload(cls.model.plan),
                joinedload(cls.model.short_link)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_short_link(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(
                cls.model
            ).where(
                cls.model.user_id == user_id,
                cls.model.is_active == True
            ).options(
                joinedload(cls.model.short_link)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_all_is_active_subscription(cls):
        async with async_session_maker() as session:
            query = select(
                cls.model
            ).where(
                cls.model.is_active == True
            ).options(
                joinedload(cls.model.user)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_subscription_joinload_in_plan(cls, subscription_id):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model
                ).where(
                    cls.model.id == subscription_id
                )
                .options(
                    joinedload(cls.model.plan)
                )
            )
            result = await session.execute(query)
            sub = result.scalars().first()
            return sub
        
    @classmethod
    async def update_expire_subsrciption(cls, now: datetime):
        async with async_session_maker() as session:
            sub_q = (
                select(User.telegram_id)
                .select_from(Subscription)
                .join(User, Subscription.user_id == User.id)
                .where(
                    Subscription.end_date <= now,
                    Subscription.is_active == True
                )
            )
            result = await session.execute(sub_q)
            telegram_ids = result.scalars().all()
            
            query = (
                update(Subscription)
                .where(
                    Subscription.end_date <= now,
                    Subscription.is_active == True
                )
                .values(is_active=False)
            )

            await session.execute(query)
            await session.commit()

            return telegram_ids

    @classmethod
    async def check_expire_subsrciption(cls, day: int):
        async with async_session_maker() as session:
            query = (
                select(User.telegram_id)
                .join(User.subscriptions)
                .filter(
                    cast(Subscription.end_date, Date) - cast(func.now(), Date) == day
                )
            )
            result = await session.execute(query)
            users = result.scalars().unique().all()

            return users


class PlanSubscriptionDAO(BaseDAO):
    model = PlanSubscription

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).where(cls.model.price > 0)
            result = await session.execute(query)
            return result.fetchall()
        
    @classmethod
    async def find_all_servers_in_plan(cls, plan_id):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.servers)).where(cls.model.id == plan_id)
            result = await session.execute(query)
            plan = result.scalars().first()
            servers = plan.servers
            return servers
        

class RefferalDAO(BaseDAO):
    model = Referral
