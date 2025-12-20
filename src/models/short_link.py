from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.utils.utils import generate_short_code, utc_now_no_microseconds


class ShortLink(Base):
    __tablename__ = "shortlinks"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    code: Mapped[str] = Column(String, unique=True, nullable=False, default=generate_short_code)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subscriptions.id", 
            ondelete="CASCADE"
        ), nullable=False
    )
    create_at: Mapped[datetime] = Column(DateTime, nullable=False, default=utc_now_no_microseconds) 

    subscription: Mapped["Subscription"] = relationship(
        "Subscription", 
        back_populates="short_link",
        foreign_keys=[subscription_id],
        lazy="select",
    )

    def __str__(self):
        return f"ShortLink #{self.id} - code: {self.code}"
