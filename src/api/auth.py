from fastapi import APIRouter, Body, HTTPException, Response

from src.exceptions import (
    IncorrectTgDataException, 
    UserSearchExcpetion,
    UserCraeateException
)
from src.services.auth import AuthService
from src.schemas.auth import TokenResponse
from src.utils.security import parse_telegram_initdata


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(init_data: str = Body(...)) -> Response:
    try:
        user_data: dict = await parse_telegram_initdata(init_data)
        token_respone: TokenResponse = await AuthService.register_and_login(
            user_data
        )
        return token_respone
    except IncorrectTgDataException as e:
        raise HTTPException(
            detail=e.detail,
            status_code=e.status_code
        )
    except UserSearchExcpetion as e:
        raise HTTPException(
            detail=e.detail,
            status_code=e.status_code
        )
    except UserCraeateException as e:
        raise HTTPException(
            detail=e.detail,
            status_code=e.status_code
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Произошла неизвестная ошибка! - {e}",
            status_code=500
        )