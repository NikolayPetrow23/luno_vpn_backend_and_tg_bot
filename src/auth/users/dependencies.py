from fastapi import Depends

from src.auth.base_depends import parse_jwt_token, get_token
from src.exceptions import UserIsNotPresentException
from src.dao.user import UserDAO

token_name = "auth_tokens"


async def get_current_user(jwt_token: str = Depends(get_token(token_name))):
    user_id: str = await parse_jwt_token(jwt_token)

    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user
