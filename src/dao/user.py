from sqlalchemy import insert, select
from src.dao.base import BaseDAO
from src.models import User

from src.database import async_session_maker

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_data(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.telegram_id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()