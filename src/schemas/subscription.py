from typing import List
from pydantic import BaseModel


class SSubscription(BaseModel):
    uuid: str
    telegram_id: int


class SXrayClient(BaseModel):
    id: str
    email: str

    @classmethod
    def from_subscription(cls, sub: SSubscription):
        return cls(id=sub.uuid, email=f"tg_{sub.telegram_id}")


class SXrayClients(BaseModel):
    users: List[SXrayClient]


class SPlanSubscription(BaseModel):
    id: int
    name: str
    price: float
    duration_days: int

    class Config:
        from_attributes = True
