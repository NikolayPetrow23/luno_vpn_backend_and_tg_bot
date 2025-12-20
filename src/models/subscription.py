from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Float, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.utils.utils import utc_now_no_microseconds


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    uuid: Mapped[str] = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan_subscriptions.id", ondelete="CASCADE")) 
    promo_code_id: Mapped[int] = mapped_column(ForeignKey("promo_codes.id", ondelete="SET NULL"), nullable=True)
    start_date: Mapped[datetime] = Column(DateTime, nullable=False, default=utc_now_no_microseconds)
    end_date: Mapped[datetime] = Column(DateTime, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="subscriptions",
        foreign_keys=[user_id],
        lazy="select"
    )
    plan: Mapped["PlanSubscription"] = relationship(
        "PlanSubscription",
        back_populates="subscription",
        foreign_keys=[plan_id],
        lazy="select"
    )
    promo_code: Mapped["PromoCode"] = relationship(
        "PromoCode",
        back_populates="subscription",
        foreign_keys=[promo_code_id],
        lazy="select"
    )
    payment: Mapped["Payment"] = relationship(
        "Payment",
        back_populates="subscription",
        lazy="select",
        uselist=False
    )
    traffic: Mapped["Traffic"] = relationship(
        "Traffic",
        back_populates="subscription",
        lazy="select",
        uselist=False
    )
    devices: Mapped[list["Device"]] = relationship(
        "Device",
        back_populates="subscription",
        lazy="selectin",
        uselist=True
    )
    short_link: Mapped["ShortLink"] = relationship(
        "ShortLink", 
        back_populates="subscription",
        lazy="select",
        uselist=False
    )

    def __str__(self):
        return f"Подписка #{self.id}, пользователь: #{self.user_id}, план: #{self.plan_id}, активна до: {self.end_date}"


class PlanSubscription(Base):
    __tablename__ = "plan_subscriptions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)
    count_devices: Mapped[int] = Column(Integer)
    duration_days: Mapped[int] = Column(Integer, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)

    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="plan")
    payment: Mapped[list["Payment"]] = relationship(
        "Payment", 
        back_populates="plan"
    )
    servers: Mapped[list["Server"]] = relationship(
        "Server",
        secondary="plan_server",
        back_populates="plans"
    )
    
    def __str__(self):
        return f"План подписки #{self.id} - {self.name}, цена: {self.price}, длительность (дней): {self.duration_days}"

class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    code: Mapped[str] = Column(String, unique=True, nullable=False)
    discount_percentage: Mapped[float] = Column(Float, nullable=False)
    valid_until: Mapped[datetime] = Column(DateTime, nullable=False, default=utc_now_no_microseconds)
    is_active: Mapped[bool] = Column(Boolean, default=True)

    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="promo_code")


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    referee_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ref_code: Mapped[str] = Column(String, nullable=False)
    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=utc_now_no_microseconds)

    # Кто пригласил
    referrer: Mapped["User"] = relationship(
        "User",
        back_populates="referrals_sent",
        foreign_keys=[referrer_id],
        lazy="select"
    )

    # Кто был приглашён (один)
    referee: Mapped["User"] = relationship(
        "User",
        back_populates="referred_by",
        uselist=False,
        foreign_keys=[referee_id],
        lazy="select"
    )
