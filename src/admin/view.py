import os
from sqladmin import ModelView
from passlib.context import CryptContext

from src.database import async_session_maker
from src.models.user import (
    User
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersAdmin(ModelView, model=User):
    column_list = [all for all in User.__table__.columns]
    column_details_exclude_list = []
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    form_excluded_columns = []
    