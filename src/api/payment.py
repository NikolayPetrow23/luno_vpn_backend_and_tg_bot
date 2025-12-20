import hmac
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from src.utils.dependencies import get_current_user
from src.models import User
from src.services.payment import PaymentService
from src.config import settings


router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/webhook/platega")
async def webhook_(request: Request):
    merchant_id = request.headers.get("X-MerchantId", "")
    secret = request.headers.get("X-Secret", "")

    if not merchant_id or not secret:
        return JSONResponse(
            status_code=400, 
            content={"detail": "Invalid headers"}
        )

    if not (
        hmac.compare_digest(merchant_id, settings.config.MERCHANT_ID)
        and hmac.compare_digest(secret, settings.config.API_KEY)
    ):
        return JSONResponse(
            status_code=403,
            content={"detail": "Unauthorized"}
        )
    
    try:
        payload = await request.json()
    except Exception as e:
        JSONResponse(
            status_code=400,
            content={"detail": "Invalid JSON"}
        )

    transaction_id = payload.get("id", "")
    status = payload.get("status", "")

    if not transaction_id or not status:
        return JSONResponse(
            status_code=400, 
            content={"detail": "Invalid payload"}
        )
    
    try:
        await PaymentService.handle_webhook_platega(
            transaction_id=transaction_id,
            status=status
        )
    except Exception as e:
        return JSONResponse(
            status_code=200,
            content={"detail": "Произошла ошибка при обработке вебхука!"}
        )

    return JSONResponse(
        status_code=200,
        content={"detail": "OK"}
    )


@router.get("")
async def create_payment(plan_id: int, payment_method: int, current_user: User = Depends(get_current_user)):
    try:
        payment_link = await PaymentService.process_payment_platega(
            plan_id=plan_id, 
            payment_method=payment_method,
            user_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    return payment_link
