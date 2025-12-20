from src.dao.user import UserDAO
from src.models import User
from src.schemas.user import SUser


class UserService:
    @staticmethod
    async def crate_user(user_data: SUser) -> bool:
        try:
            user_exists: User | None = await UserDAO.find_one_or_none(
                telegram_id=user_data.telegram_id
            )
            if user_exists:
                return False
            
            await UserDAO.add_data(
                telegram_id=user_data.telegram_id,
                username=user_data.username,
                first_name=user_data.first_name
            )
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False