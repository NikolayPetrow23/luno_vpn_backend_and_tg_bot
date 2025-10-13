from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String,  Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ip_address: Mapped[str] = Column(String, unique=True, nullable=False)
    location: Mapped[str] = Column(String, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    capacity: Mapped[int] = Column(Integer, nullable=False)

    vpn_configuration: Mapped[list["VPNConfiguration"]] = relationship(
        "VPNConfiguration", 
        back_populates="server",
        foreign_keys="[VPNConfiguration.server_id]",
        lazy="select"
    )


class VPNConfiguration(Base):
    __tablename__ = "vpn_configurations"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    server_id: Mapped[int] = mapped_column(ForeignKey("servers.id", ondelete="CASCADE"))
    config_data: Mapped[str] = Column(String, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False, default=datetime.now)


    user: Mapped["User"] = relationship(
        "User", 
        back_populates="vpn_configuration",
        foreign_keys=[user_id],
        lazy="select"
    )
    server: Mapped["Server"] = relationship(
        "Server", 
        back_populates="vpn_configuration",
        foreign_keys=[server_id],
        lazy="select"
    )
