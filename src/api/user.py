from fastapi import APIRouter, Depends

from src.utils.dependencies import get_current_user
from src.models.user import User


router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user.telegram_id