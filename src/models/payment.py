from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.models.enum import PaymentStatus
from src.utils.utils import utc_now_no_microseconds


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
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
        ), nullable=True
    )
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan_subscriptions.id", ondelete="CASCADE")) 
    transaction_id: Mapped[str] = Column(String, unique=True, nullable=False)
    amount: Mapped[float] = Column(Float, nullable=False)
    income_amount: Mapped[float] = Column(Float, nullable=False)
    currency: Mapped[str] = Column(String, nullable=False)
    status: Mapped[bool] = Column(SQLAlchemyEnum(PaymentStatus), nullable=False, default=PaymentStatus.CREATED)
    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=utc_now_no_microseconds) 

    user: Mapped["User"] = relationship(
        "User", 
        back_populates="payments",
        foreign_keys=[user_id],
        lazy="select"
    )
    payment_type: Mapped["PaymentType"] = relationship(
        "PaymentType", 
        back_populates="payments",
        foreign_keys=[payment_type_id],
        lazy="select"
    )
    subscription: Mapped["Subscription"] = relationship(
        "Subscription", 
        back_populates="payment",
        foreign_keys=[subscription_id],
        lazy="select",
    )
    plan: Mapped["PlanSubscription"] = relationship(
        "PlanSubscription",
        back_populates="payment",
        foreign_keys=[plan_id],
        lazy="select"
    ) 

    def __str__(self):
        return f"Платеж #{self.id} - пользователь: #{self.user_id}, сумма: {self.amount}({self.income_amount}) {self.currency}, статус: {'успешен' if self.status else 'неуспешен'}"


class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    code: Mapped[int] = Column(Integer, unique=True, nullable=False)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    commission_percentage: Mapped[float] = Column(Float, nullable=False)

    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="payment_type")

    def __str__(self):
        return f"Тип платежа #{self.id} - {self.name}, комиссия: {round(self.commission_percentage * 100, 1)}%"
    