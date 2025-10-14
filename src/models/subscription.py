from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Float, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan_subscriptions.id", ondelete="CASCADE")) 
    promo_code_id: Mapped[int] = mapped_column(ForeignKey("promo_codes.id", ondelete="SET NULL"), nullable=True)
    start_date: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
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


class PlanSubscription(Base):
    __tablename__ = "plan_subscriptions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)
    duration_days: Mapped[int] = Column(Integer, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)

    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="plan")


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    code: Mapped[str] = Column(String, unique=True, nullable=False)
    discount_percentage: Mapped[float] = Column(Float, nullable=False)
    valid_until: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)
    is_active: Mapped[bool] = Column(Boolean, default=True)

    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="promo_code")


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    referee_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ref_code: Mapped[str] = Column(String, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)

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
