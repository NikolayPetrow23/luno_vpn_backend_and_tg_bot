import asyncio
import sys


sys.path.append('')

from src.models import User, UserRole
from src.dao.user import UserDAO
from src.auth.auth import get_password_hash


async def create_superuser(
    username: str, 
    first_name: str,
    password: str
):  
    user: User | None = await UserDAO.find_one_or_none(username=username)

    if user:
        print("Пользователь уже существует")
        return
    
    hashed_password = get_password_hash(password)

    try:
        await UserDAO.add_data(
            telegram_id=11434010011,
            username=username,
            hashed_password=hashed_password,
            first_name=first_name,
            role=UserRole.ADMIN,
            is_testing_subscribe=True,
            is_active=True
        )

        print(f"Суперпользователь {username} создан!")
    except Exception as e:
        print(f"Произошла ошибка при создании суперпользователя: {e}")

if __name__ == "__main__":
    username = input("Username суперюзера: ")
    first_name = input("Имя суперюзера: ")
    password = input("Пароль суперюзера: ")
    asyncio.run(
        create_superuser(
            username=username, 
            first_name=first_name, 
            password=password
        )
    )
