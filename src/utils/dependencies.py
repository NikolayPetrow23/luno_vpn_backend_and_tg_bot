import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.dao.user import UserDAO
from src.config import settings
from src.exceptions import (
    IncorrectTokenException,
    TokenExpiredException,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.config.JWT_SECRET_KEY,
            algorithms=[settings.config.ALGORITHM]
        )
        user_telegram_id = payload.get("sub")
        exp = payload.get("exp")

        if user_telegram_id is None:
            raise IncorrectTokenException

        now: datetime = datetime.datetime.now(datetime.timezone.utc)
        expiry: datetime = datetime.datetime.fromtimestamp(exp, datetime.timezone.utc)

        if now > expiry:
            raise TokenExpiredException
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен!")

    user = await UserDAO.find_one_or_none(telegram_id=user_telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователя не существует!")

    return user