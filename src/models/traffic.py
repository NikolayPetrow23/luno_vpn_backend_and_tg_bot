from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Float, BIGINT
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

class Traffic(Base):
    __tablename__ = "traffic"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subscriptions.id", 
            ondelete="CASCADE"
        ), nullable=False
    )
    uplink: Mapped[int] = Column(BIGINT, nullable=True)
    downlink: Mapped[int] = Column(BIGINT, nullable=True)
    updated_at: Mapped[datetime] = Column(DateTime)

    subscription: Mapped["Subscription"] = relationship(
        "Subscription", 
        back_populates="traffic",
        foreign_keys=[subscription_id],
        lazy="select",
    )