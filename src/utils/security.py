from init_data_py import InitData
from passlib.context import CryptContext

from src.exceptions import IncorrectTgDataException
from src.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def parse_telegram_initdata(init_data: str) -> dict:
    """
    Проверяет подпись Telegram и возвращает чистый словарь с user data.
    """

    try:
        init_data = InitData.parse(init_data)  
        init_data.validate(
            bot_token=settings.config.BOT_TOKEN,
            lifetime=3600,
        )
    except Exception as e:
        raise IncorrectTgDataException.set_detail(
            f"В процессе проверки данных telegram произошла ошибка! Exception - {e}"
        )

    user_data: dict = {
        "telegram_id": str(init_data.user.id),
        "username": init_data.user.username,
        "first_name": init_data.user.first_name,
    }

    return user_data
