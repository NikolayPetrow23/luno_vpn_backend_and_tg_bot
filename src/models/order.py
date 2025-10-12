from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[datetime] = Column(DateTime, nullable=False)
    total_price: Mapped[int] = Column(Integer, nullable=False)
    # status: Mapped[str] = Column(SQLAlchemyEnum(StatusOrderEnum), nullable=False, default=StatusOrderEnum.CREATED)
    date_create: Mapped[datetime] = Column(DateTime, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="orders")
