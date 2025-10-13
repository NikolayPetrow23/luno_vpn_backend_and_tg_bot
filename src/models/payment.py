from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    payment_provider_id: Mapped[int] = mapped_column(
        ForeignKey(
            "payment_providers.id", 
            ondelete="CASCADE"
        ), nullable=False
    )
    payment_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            "payment_types.id", 
            ondelete="CASCADE"
        ), nullable=False
    )
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subscriptions.id", 
            ondelete="CASCADE"
        ), nullable=False
    )
    transaction_id: Mapped[str] = Column(String, unique=True, nullable=False)
    amount: Mapped[float] = Column(Integer, nullable=False)
    currency: Mapped[str] = Column(String, nullable=False)
    status: Mapped[bool] = Column(Boolean, default=False)
    crate_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now) 

    user: Mapped["User"] = relationship(
        "User", 
        back_populates="payments",
        foreign_keys=[user_id],
        lazy="select"
    )
    payment_provider: Mapped["PaymentProvider"] = relationship(
        "PaymentProvider", 
        back_populates="payments",
        foreign_keys=[payment_provider_id],
        lazy="select"
    )
    payment_type: Mapped["PaymentType"] = relationship(
        "PaymentType", 
        back_populates="payments",
        foreign_keys=[payment_type_id],
        lazy="select"
    )


class PaymentProvider(Base):
    __tablename__ = "payment_providers"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    commission_percentage: Mapped[float] = Column(Float, nullable=False)
    web_hook_url: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)

    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="payment_provider")


class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    commission_percentage: Mapped[float] = Column(Float, nullable=False)

    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="payment_type")
