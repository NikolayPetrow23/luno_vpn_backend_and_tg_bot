import datetime
from jose import JWTError, jwt
from src.dao.user import UserDAO
from src.exceptions import (
    IncorrectEmailOrPasswordException,
    IncorrectTokenException, 
    TokenExpiredException,
    UserAlreadyExistsException,
    UserIsNotPresentException
)
from src.schemas.auth import TokenResponse
from src.config import settings
from src.utils.jwt_handler import create_access_token


class AuthService:
    @staticmethod
    async def register_and_login(user_data: dict) -> TokenResponse:
        existing_user = await UserDAO.find_one_or_none(
            telegram_id=user_data.get("telegram_id")
        )

        if existing_user:
            user_id = existing_user.telegram_id
        else:
            new_user_telegram_id: str = await UserDAO.add_data(
                telegram_id=user_data.get("telegram_id"),
                username=user_data.get("username"),
                first_name=user_data.get("first_name")
            )
            user_id = new_user_telegram_id
        access_token = create_access_token({"sub": user_id})

        return TokenResponse(access_token=access_token)
