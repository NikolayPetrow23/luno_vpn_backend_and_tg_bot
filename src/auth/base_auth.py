from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from src.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def encode_jwt_token(
    payload: dict,
    key: str = settings.config.ACCESS_SECRET_KEY,
    algorithm: str = settings.config.ALGORITHM,
    expire_days: int = settings.auth_jwt.access_token_expire_days,
) -> str:
    to_encode = payload.copy()
    now = datetime.now()

    expire = now + timedelta(days=expire_days)

    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded_jwt = jwt.encode(
        to_encode,
        key,
        algorithm,
    )
    
    return encoded_jwt


def encode_token_user_id(
    payload: dict,
    key: str = settings.config.ACCESS_SECRET_KEY,
    algorithm: str = settings.config.ALGORITHM
):
    to_encode = payload.copy()

    encoded_jwt = jwt.encode(
        to_encode,
        key,
        algorithm
    )

    return encoded_jwt


def decode_jwt(
    token: str,
    key: str,
    algorithm: str = settings.config.ALGORITHM,
) -> dict:
    try:
        decoded = jwt.decode(
            token,
            key,
            algorithm,
        )
        return decoded
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")
