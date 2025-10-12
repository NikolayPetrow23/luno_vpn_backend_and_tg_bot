from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError
from fastapi.responses import RedirectResponse

from src.config import settings
from src.auth.base_auth import decode_jwt
from src.exceptions import (TokenAbsentException, TokenExpiredException,
                            IncorrectTokenException)


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

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    return sub
