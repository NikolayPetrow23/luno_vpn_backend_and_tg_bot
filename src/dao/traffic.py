from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload, joinedload
from src.dao.base import BaseDAO
from src.models import Traffic, Subscription

from src.database import async_session_maker

class TrafficDAO(BaseDAO):
    model = Traffic

    @classmethod
    async def update_traffic_in_subscription_is_active(cls, increment: int):
        async with async_session_maker() as session:
            sub_q = select(Subscription.id).where(
                Subscription.is_active == True
            )
            query = update(Traffic).where(Traffic.subscription_id.in_(sub_q)).values(downlink=Traffic.downlink + increment)
                
            await session.execute(query)
            await session.commit()
