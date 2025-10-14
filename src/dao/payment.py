from sqlalchemy import insert, select
from src.dao.base import BaseDAO
from src.models import Payment

from src.database import async_session_maker


class PaymentDAO(BaseDAO):
    model = Payment

    @classmethod
    async def find_last(cls, **data) -> int:
        async with async_session_maker() as session:
            query = select(cls.model).order_by(cls.model.id.desc()).limit(1)
            result = await session.execute(query)
            return result.scalar_one_or_none()
