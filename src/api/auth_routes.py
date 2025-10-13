from fastapi import APIRouter

from src.dao.user import UserDAO
from src.schemas.auth import SUserAuth


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(telegram_id=user_data.telegram_id)
    if existing_user:
        return existing_user.id
    user_id: int = await UserDAO.add_data(
        telegram_id=user_data.telegram_id, 
        username=user_data.username,
        first_name=user_data.first_name
    )
    return user_id