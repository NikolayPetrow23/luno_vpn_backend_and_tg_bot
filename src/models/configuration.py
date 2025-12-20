from datetime import datetime

from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.enum import UserRole
from src.database import Base


class Configuration(Base):
    __tablename__ = "configurations"

    id: Mapped[int] = Column(Integer, primary_key=True)
    reward_ref: Mapped[int] = Column(Integer, nullable=False)
    increment: Mapped[int] = Column(Integer, nullable=False)
