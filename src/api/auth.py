from fastapi import APIRouter, Body, HTTPException

from src.exceptions import UserAlreadyExistsException
from src.services.auth import AuthService
from src.dao.user import UserDAO
from src.schemas.auth import SUserAuth
from src.utils.security import parse_telegram_initdata


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(init_data: str = Body(...)):
    try:
        try:
            user_data = await parse_telegram_initdata(init_data)
        except Exception as e:
            return {"detail": "Ошибка при проверки initData", "error": str(e)}
        
        user_telegram_id = await AuthService.register_and_login(
            user_data
        )
        return {"detail": "Пользователь успешно прошел проверку!", "user_telegram_id": user_telegram_id}
    
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=e.detail)
