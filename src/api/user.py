from fastapi import APIRouter, Depends, Request

from src.utils.dependencies import get_current_user
from src.models import User


router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
