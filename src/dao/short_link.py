from sqlalchemy import insert, select
from src.dao.base import BaseDAO
from src.models import ShortLink

from src.database import async_session_maker


class ShortLinkDAO(BaseDAO):
    model = ShortLink
