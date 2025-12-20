from sqlalchemy import insert, select, func
from sqlalchemy.orm import selectinload, joinedload
from src.dao.base import BaseDAO
from src.models import Device

from src.database import async_session_maker


class DeviceDAO(BaseDAO):
    model = Device

    @classmethod
    async def find_count_devices_in_sub_or_none(cls, subscription_id: int):
        async with async_session_maker() as session:
            query = select(
                func.count(cls.model.id)
            ).filter_by(
                subscription_id=subscription_id
            )

            res = await session.execute(query)
            result = res.scalar_one_or_none()
            return result
