from fastapi import APIRouter

from src.api.user_routes import router as router_user


router = APIRouter(prefix="/api/v1", tags=["API V1"])
router.include_router(router_user)
