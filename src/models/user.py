from datetime import datetime

from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, unique=True, nullable=False)
    phone_number: Mapped[str] = Column(String, unique=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    date_create: Mapped[datetime] = Column(DateTime, nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")