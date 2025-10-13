from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    telegram_id: str
    username: str
    first_name: EmailStr
