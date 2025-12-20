from pydantic import BaseModel


class SUser(BaseModel):
    telegram_id: int
    username: str
    first_name: str
