import datetime
from jose import jwt
from src.models import User
from src.dao.user import UserDAO
from src.exceptions import UserSearchExcpetion, UserCraeateException
from src.schemas.auth import TokenResponse
from src.config import settings
from src.utils.jwt_handler import create_access_token
from src.utils.utils import generate_short_code


class AuthService:
    @staticmethod
    async def register_and_login(user_data: dict) -> TokenResponse:
        telegram_id: int = int(user_data.get("telegram_id", ""))
        try:
            user: User | None = await UserDAO.find_one_or_none(
                telegram_id=telegram_id
            )
        except Exception as e:
            raise UserSearchExcpetion.set_detail(
                f"Ошибка в поиски пользователя! Ошибка - {e}"
            )
        if user is None:
            ref_code: str = generate_short_code()
            try:
                user: User = await UserDAO.add_data(
                    telegram_id=int(user_data.get("telegram_id")),
                    username=user_data.get("username"),
                    first_name=user_data.get("first_name"),
                    ref_code=ref_code
                )
            except Exception as e:
                raise UserCraeateException.set_detail(
                    f"Ошибка при создании пользователя! Ошибка - {e}"
                )
        access_token: str = create_access_token({"sub": str(user.telegram_id)})
        return TokenResponse(access_token=access_token)
