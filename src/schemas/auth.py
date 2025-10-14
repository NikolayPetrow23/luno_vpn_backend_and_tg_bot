from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    telegram_id: str
    username: str
    first_name: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
