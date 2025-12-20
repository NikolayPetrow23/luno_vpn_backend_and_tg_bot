from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Enum as SQLAlchemyEnum, BigInteger, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.enum import UserRole
from src.database import Base
from src.utils.utils import generate_short_code, utc_now_no_microseconds


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    telegram_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = Column(String, unique=True, nullable=True)
    ref_code: Mapped[str] = Column(String, unique=True, nullable=True, default=generate_short_code)
    hashed_password: Mapped[bytes] = Column(LargeBinary, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.CLIENT) 
    is_testing_subscribe: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=utc_now_no_microseconds)

    # Приглашенные этим пользователем (много)
    referrals_sent: Mapped[list["Referral"]] = relationship(
        "Referral",
        back_populates="referrer",
        lazy="select",
        cascade="all, delete-orphan",
        foreign_keys="[Referral.referrer_id]"
    )
    # Пользователь, который пригласил этого юзера (один)
    referred_by: Mapped["Referral"] = relationship(
        "Referral",
        back_populates="referee",
        uselist=False,
        foreign_keys="[Referral.referee_id]",
        lazy="select"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", 
        back_populates="user",
        foreign_keys="[Subscription.user_id]",
        lazy="select"
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment", 
        back_populates="user",
        foreign_keys="[Payment.user_id]",
        lazy="select"
    )   

    def __str__(self):
        return f"Пользователь #{self.id} - telegram_id: {self.telegram_id}"
