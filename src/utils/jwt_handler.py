import datetime
from jose import jwt
from src.config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(minutes=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.config.JWT_SECRET_KEY, settings.config.ALGORITHM)
    return encoded_jwt
