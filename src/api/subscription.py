import base64
from fastapi import APIRouter, Depends, HTTPException

from src.exceptions import SubscriptionActiveException, PlanNotFound, ShortLinkNotFound
from src.models.short_link import ShortLink
from src.utils.dependencies import get_current_user
from src.services.subscribtion import SubscriptionService
from src.schemas.auth import SUser
from src.config import settings

router = APIRouter(prefix="/subscription", tags=["Subscription"])


@router.get("/plans")
async def subscription_plans():
    try:
        plans_subscription = await SubscriptionService.plan_subscription()
        return plans_subscription
    except PlanNotFound as e:
        return HTTPException(
            status_code=e.status_code, detail=e.detail
        )
    except Exception as e:
        return HTTPException(
            status_code=500, detail=f"Произошла неизвестная ошибка!"
        )

@router.get("/short-link")
async def subscription_short_link(current_user: SUser = Depends(get_current_user)) -> str:
    try:
        short_code: ShortLink | None = await SubscriptionService.get_short_link(user_id=current_user.id)
        short_link = f"https://{settings.config.URL_DOMAIN_SUB}/{short_code}" if short_code else f"short_link не найден!"
        return short_link
    except ShortLinkNotFound as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Произошла неизвестная ошибка!"
        )


@router.get("/me")
async def subscription_me(current_user: SUser = Depends(get_current_user)):
    try:
        subscription = await SubscriptionService.subsription_plan_user(user_id=current_user.id)
        return subscription
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Произошла неизвестная ошибка!"
        )


@router.post("/activate/testing")
async def subscription(current_user: SUser = Depends(get_current_user)):
    try:
        subscription = await SubscriptionService.activate_testing_subscribe(user_id=current_user.id)
        return subscription
    except SubscriptionActiveException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except PlanNotFound as e:
        raise HTTPException(
            status_code=e.status_code, detail=e.detail
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail=f"Произошла неизвестная ошибка! - {e}"
        )