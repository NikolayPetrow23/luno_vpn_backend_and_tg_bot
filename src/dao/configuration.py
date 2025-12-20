from sqlalchemy import select
from src.dao.base import BaseDAO
from src.models import Configuration

from src.database import async_session_maker


class ConfigurationDAO(BaseDAO):
    model = Configuration

    @classmethod
    async def find_config(cls):
        async with async_session_maker() as session:
            query = select(
                cls.model
            ).where(
                cls.model.id == 1
            )

            res = await session.execute(query)
            result = res.scalar_one_or_none()
            return result