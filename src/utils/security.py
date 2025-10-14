from init_data_py import InitData
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def parse_telegram_initdata(init_data: str) -> dict:
    """
    Проверяет подпись Telegram и возвращает чистый словарь с user data.
    """

    init_data = InitData.parse(init_data)

    user_data = {
        "telegram_id": str(init_data.user.id),
        "username": init_data.user.username,
        "first_name": init_data.user.first_name,
    }

    return user_data
