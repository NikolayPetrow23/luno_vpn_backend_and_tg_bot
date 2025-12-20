import enum


class UserRole(enum.Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    CLIENT = "Client"


class PaymentStatus(enum.Enum):
    NONE = "NONE"
    CREATED = "CREATED"
    PENDING = "PENDING"
    INPROGRESS = "INPROGRESS"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELED = "CANCELED"
    CONFIRMED = "CONFIRMED"
    REFUNDED = "REFUNDED"
    CHARGEBACKED = "CHARGEBACKED"
    OTHER = "OTHER"
