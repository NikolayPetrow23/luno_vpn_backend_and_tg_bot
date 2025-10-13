from fastapi import APIRouter

from src.api.user_routes import router as router_user
from src.api.auth_routes import router as router_auth


router = APIRouter(prefix="/api/v1")
router.include_router(router_user)
router.include_router(router_auth)
