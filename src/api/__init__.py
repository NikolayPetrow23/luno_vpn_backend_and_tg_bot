from fastapi import APIRouter

from src.api.user import router as router_user
from src.api.auth import router as router_auth
from src.api.payment import router as router_payment
from src.api.subscription import router as router_subscription


router = APIRouter(prefix="/api/v1")
router.include_router(router_user)
router.include_router(router_auth)
router.include_router(router_payment)
router.include_router(router_subscription)
