from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError

from src.exceptions import UserIsNotPresentException
from src.auth.dependencies import parse_jwt_token
from src.dao.user import UserDAO

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

async def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid auth scheme")
        
        payload = await parse_jwt_token(token)

        telegram_id = payload.get("user_id")

        user = await UserDAO.find_by_id(str(telegram_id))

        if not user or user_id is None:
            raise UserIsNotPresentException

        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    

async def get_current_user(jwt_token: str = Depends(get_token(token_name))):
    user_id: str = await parse_jwt_token(jwt_token)

    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user


def get_token(token_name: str):
    def dependency(request: Request) -> str:
        jwt_token = request.cookies.get(token_name)

        if jwt_token:
            return jwt_token

        raise TokenAbsentException
    
    return dependency