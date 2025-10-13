import enum


class PlanSubscribeEnum(enum.Enum):
    PROMO = "Promo"
    STANDART = "Standart"
    PRO = "Pro"


class UserRole(enum.Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    CLIENT = "Client"
