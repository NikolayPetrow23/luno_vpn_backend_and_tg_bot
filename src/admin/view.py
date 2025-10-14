import os
from sqladmin import ModelView
from passlib.context import CryptContext

from src.database import async_session_maker
from src.models import (
    User, Subscription, PlanSubscription, PromoCode, Referral, 
    Payment, PaymentProvider, PaymentType, VPNConfiguration, Server
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
    

class PlansAdmin(ModelView, model=PlanSubscription):
    column_list = [all for all in PlanSubscription.__table__.columns]
    column_details_exclude_list = []
    can_delete = True
    name = "План подписки"
    name_plural = "Планы подписок"
    icon = "fa-solid fa-list"
    form_excluded_columns = [PlanSubscription.subscription]


class SubscriptionsAdmin(ModelView, model=Subscription):
    column_list = [all for all in Subscription.__table__.columns]
    column_details_exclude_list = []
    can_delete = True
    name = "Подписка"
    name_plural = "Подписки"
    icon = "fa-solid fa-list"
    form_excluded_columns = []


class PaymentAdmin(ModelView, model=Payment):
    column_list = [all for all in Payment.__table__.columns]
    column_details_exclude_list = []
    can_delete = True
    name = "Платеж"
    name_plural = "Платежи"
    icon = "fa-solid fa-credit-card"
    form_excluded_columns = []
