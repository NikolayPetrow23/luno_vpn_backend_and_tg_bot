from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    domain: Mapped[str] = Column(String, unique=True, nullable=False)
    ip_address: Mapped[str] = Column(String, unique=True, nullable=False)
    port: Mapped[int] = Column(Integer, nullable=False)  
    pbk: Mapped[str] = Column(String, nullable=True)
    sid: Mapped[str] = Column(String, nullable=True)
    location: Mapped[str] = Column(String, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    emoji: Mapped[str] = Column(String, nullable=False)  

    plans: Mapped[list["PlanSubscription"]] = relationship(
        "PlanSubscription",
        secondary="plan_server",
        back_populates="servers"
    )

    def __str__(self):
        return f"Сервер #{self.id}, {self.location}{self.emoji}"



class PlanServer(Base):
    __tablename__ = "plan_server"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan_subscriptions.id", ondelete="CASCADE"))
    server_id: Mapped[int] = mapped_column(ForeignKey("servers.id", ondelete="CASCADE"))


class HeadersConfigVPN(Base):
    __tablename__ = "headers_vpn_config"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    profile_title: Mapped[str] = Column(String, unique=True, nullable=False)
    announce: Mapped[str] = Column(String, unique=True, nullable=False)
    profile_web_page_url: Mapped[str] = Column(String, unique=True, nullable=False)
    support_url: Mapped[str] = Column(String, unique=True, nullable=False)
    profile_update_interval: Mapped[str] = Column(String, unique=True, nullable=False)
