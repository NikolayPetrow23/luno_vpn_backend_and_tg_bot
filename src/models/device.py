from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subscriptions.id", 
            ondelete="CASCADE"
        ), nullable=False
    )
    identifier_type_id: Mapped[int] = Column(Integer, ForeignKey("device_identifier_types.id", ondelete="RESTRICT"))
    identifier_value: Mapped[str] = Column(String, nullable=False)
    device_model: Mapped[str] = Column(String, nullable=False)
    ip: Mapped[str] = Column(String, nullable=True)
    last_connected: Mapped[datetime] = Column(DateTime)

    subscription: Mapped["Subscription"] = relationship(
        "Subscription", 
        back_populates="devices",
        foreign_keys=[subscription_id],
        lazy="select"
    )
    identifier_type: Mapped["DeviceIdentifierType"] = relationship(
        "DeviceIdentifierType", 
        back_populates="devices",
        foreign_keys=[identifier_type_id],
        lazy="select"
    )


class DeviceIdentifierType(Base):
    __tablename__ = "device_identifier_types"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, nullable=False)

    devices: Mapped[list["Device"]] = relationship(
        "Device",
        back_populates="identifier_type",
        lazy="selectin",
        uselist=True
    )
