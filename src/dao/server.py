from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload, joinedload
from src.dao.base import BaseDAO
from src.models import Server

from src.database import async_session_maker

class ServerDAO(BaseDAO):
    model = Server

    @classmethod
    async def find_servers_is_active_in_domain(cls):
        async with async_session_maker() as session:
            query = select(
                cls.model.domain
            ).filter_by(
                is_active=True
            )

            result = await session.execute(query)
            return result.scalars().all()
