from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from src.auth.auth import encode_jwt_token, validate_password
from src.admin.utils import get_current_user
from src.config import settings
from src.models.user import User, UserRole
from src.dao.user import UserDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not username or not password:
            return False

        user: User | None = await UserDAO.find_one_or_none(username=username)

        if not user:
            return False
        
        if user.role != UserRole.ADMIN:
            return False
        
        if not user.hashed_password or not validate_password(password, user.hashed_password):
            return False

        access_token = encode_jwt_token({"sub": str(user.id)})
        request.session.update({"token": access_token})

        return True
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key="...")
