import os
from sqladmin import ModelView
from passlib.context import CryptContext

from src.database import async_session_maker
from src.models import (
    User, Subscription, PlanSubscription, PromoCode, Referral, 
    Payment, PaymentType, Server, Traffic, 
    ShortLink, Device, HeadersConfigVPN, DeviceIdentifierType,
    PlanServer, Configuration
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersAdmin(ModelView, model=User):
    column_list = [User.id, User.telegram_id, User.username, User.is_testing_subscribe] + [User.subscriptions, User.payments]
    column_details_exclude_list = []
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    form_excluded_columns = []


class ConfigurationAdmin(ModelView, model=Configuration):
    column_list = [all for all in Configuration.__table__.columns]
    column_details_exclude_list = []
    name = "Кофиг"
    name_plural = "Конфигурация"
    icon = "fa-solid fa-network-wired"
    form_excluded_columns = []


class PromoCodeAdmin(ModelView, model=PromoCode):
    column_list = [all for all in PromoCode.__table__.columns]
    column_details_exclude_list = []
    name = "Промокод"
    name_plural = "Промокоды"
    icon = "fa-solid fa-percent"
    form_excluded_columns = []
    

class ReferralAdmin(ModelView, model=Referral):
    column_list = [Referral.id, Referral.referrer, Referral.referee, Referral.ref_code, Referral.create_at]
    column_details_exclude_list = []
    name = "Реферал"
    name_plural = "Рефералы"
    icon = "fa-solid fa-users"
    form_excluded_columns = []


class PlansAdmin(ModelView, model=PlanSubscription):
    column_list = [all for all in PlanSubscription.__table__.columns] + ["servers"]
    column_details_exclude_list = []
    name = "План подписки"
    name_plural = "Планы подписок"
    icon = "fa-solid fa-list"
    form_excluded_columns = [PlanSubscription.subscription]


class PlanServersAdmin(ModelView, model=PlanServer):
    column_list = ["server_id", "plan_id"]
    column_details_exclude_list = []
    name = "Планы и сервер"
    name_plural = "Планы и сервера"
    icon = "fa-solid fa-list"


class SubscriptionsAdmin(ModelView, model=Subscription):
    column_list = [Subscription.id, Subscription.user, Subscription.is_active, Subscription.payment, Subscription.start_date, Subscription.end_date, Subscription.short_link]
    column_details_exclude_list = []
    name = "Подписка"
    name_plural = "Подписки"
    icon = "fa-solid fa-receipt"
    form_excluded_columns = []


class PaymentAdmin(ModelView, model=Payment):
    column_list = [Payment.id, Payment.transaction_id, Payment.income_amount, Payment.status, Payment.user, Payment.subscription, Payment.plan]
    column_details_exclude_list = []
    name = "Платеж"
    name_plural = "Платежи"
    icon = "fa-solid fa-credit-card"
    form_excluded_columns = []


class PaymentTypeAdmin(ModelView, model=PaymentType):
    column_list = [all for all in PaymentType.__table__.columns]
    column_details_exclude_list = []
    name = "Тип платежа"
    name_plural = "Типы платежей"
    icon = "fa-solid fa-file-invoice-dollar"
    form_excluded_columns = [PaymentType.payments]


class DeviceAdmin(ModelView, model=Device):
    column_list = [all for all in Device.__table__.columns]
    column_details_exclude_list = []
    name = "Девайс"
    name_plural = "Девайсы"
    icon = "fa-solid fa-display"


class DeviceIdentifierTypeAdmin(ModelView, model=DeviceIdentifierType):
    column_list = [all for all in DeviceIdentifierType.__table__.columns]
    column_details_exclude_list = []
    can_delete = True
    name = "Тип идентификатора устройства"
    name_plural = "Типы идентификатора устройства"
    icon = "fa-solid fa-align-left"


class TrafficAdmin(ModelView, model=Traffic):
    column_list = [all for all in Traffic.__table__.columns]
    column_details_exclude_list = []
    can_delete = True
    name = "Траффик"
    name_plural = "Траффик"
    icon = "fa-solid fa-arrow-right-arrow-left"


class ShortLinkAdmin(ModelView, model=ShortLink):
    column_list = [all for all in ShortLink.__table__.columns] + [ShortLink.subscription]
    column_details_exclude_list = []
    can_delete = True
    name = "Быстрая ссылка"
    name_plural = "Быстрые ссылки"
    icon = "fa-solid fa-link"


class HeadersConfigVPNAdmin(ModelView, model=HeadersConfigVPN):
    column_list = [all for all in HeadersConfigVPN.__table__.columns]
    column_details_exclude_list = []
    can_delete = True
    name = "Заголовок для конфигурации"
    name_plural = "Заголовоки для конфигурации"
    icon = "fa-solid fa-gear"


class ServerAdmin(ModelView, model=Server):
    column_list = [all for all in Server.__table__.columns] + ["plans"]
    column_details_exclude_list = []
    can_delete = True
    name = "Сервер"
    name_plural = "Серверы"
    icon = "fa-solid fa-server"