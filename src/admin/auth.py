from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from src.auth.auth import encode_jwt_token
from src.admin.utils import get_current_user
from src.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == "nik@mail.ru" and password == "123456":
            access_token = encode_jwt_token({"sub": str(1)})
            request.session.update({"token": access_token})
            token = request.session.get("token")
            print("Admin session token:", token)
            return True
        return False 

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
