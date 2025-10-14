from fastapi import APIRouter

from src.services.subscribtion import SubscriptionService
from src.dao.user import UserDAO
from src.schemas.auth import SUserAuth


router = APIRouter(prefix="/subscription", tags=["Subsctiption"])


@router.get("/")
async def subscription():
    ...


@router.get("/plans")
async def plans():
    plans_subscription = await SubscriptionService.plan_subscription()
    return plans_subscription