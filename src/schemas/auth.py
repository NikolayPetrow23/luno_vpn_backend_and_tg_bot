from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    telegram_id: str
    username: str
    first_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    tg_data: str
