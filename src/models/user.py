from datetime import datetime

from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.enum import UserRole
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    telegram_id: Mapped[str] = Column(String, unique=True, nullable=False)
    username: Mapped[str] = Column(String, unique=True, nullable=True)
    hashed_password: Mapped[bytes] = Column(LargeBinary, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.CLIENT) 
    is_active: Mapped[bool] = Column(Integer, nullable=False, default=True)
    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)

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
    vpn_configuration: Mapped[list["VPNConfiguration"]] = relationship(
        "VPNConfiguration", 
        back_populates="user",
        foreign_keys="[VPNConfiguration.user_id]",
        lazy="select"
    )
