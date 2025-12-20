from sqlalchemy import insert, select, exists
from src.dao.base import BaseDAO
from src.models import User, Subscription

from src.database import async_session_maker

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_data(cls, **data) -> str:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()    

    @classmethod
    async def find_all_users_in_telegram_id(cls) -> list[int]:
        async with async_session_maker() as session:
            query = select(cls.model.telegram_id)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def find_not_is_active_users_in_telegram_id(cls) -> list[int]:
        async with async_session_maker() as session:
            sub_active_exists = (
                select(1)
                .where(
                    Subscription.user_id == User.id,
                    Subscription.is_active == True
                )
            )

            query = (
                select(User.telegram_id)
                .where(~exists(sub_active_exists))
            )
            result = await session.execute(query)
            return result.scalars().all()