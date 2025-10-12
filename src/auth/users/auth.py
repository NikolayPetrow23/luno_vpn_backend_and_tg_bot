from pydantic import EmailStr
from fastapi import Response

from src.auth.base_auth import validate_password, encode_jwt_token
from src.exceptions import IncorrectEmailOrPasswordException
from src.models import User
from src.dao.user import UserDAO


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)

    if user and validate_password(password, user.hashed_password):
        return user
    raise IncorrectEmailOrPasswordException


async def set_cookie_user(response: Response, user: User):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.name,
        "email": user.email,
    }
    access_token = encode_jwt_token(jwt_payload)

    response.set_cookie(
        "auth_tokens",
        access_token,
        httponly=True
    )
