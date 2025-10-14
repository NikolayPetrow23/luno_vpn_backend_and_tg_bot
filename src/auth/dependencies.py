from fastapi import Depends

from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError
from fastapi.responses import RedirectResponse



from src.config import settings
from src.auth.auth import decode_jwt
from src.exceptions import (TokenAbsentException, TokenExpiredException,
                            IncorrectTokenException)
from src.exceptions import UserIsNotPresentException
from src.dao.user import UserDAO

token_name = "auth_telegram_token"


def get_token(token_name: str):
    def dependency(request: Request) -> str:
        jwt_token = request.cookies.get(token_name)

        if jwt_token:
            return jwt_token

        raise TokenAbsentException
    
    return dependency


async def parse_jwt_token(jwt_token: str) -> str:
    try:
        payload = decode_jwt(
            jwt_token,
            settings.config.ACCESS_SECRET_KEY
        )
    except JWTError:
        raise IncorrectTokenException

    expire: str = payload.get("exp")
    sub: str = payload.get("sub")

    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException

    return sub


async def get_current_user(jwt_token: str = Depends(get_token(token_name))):
    user_id: str = await parse_jwt_token(jwt_token)

    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user
