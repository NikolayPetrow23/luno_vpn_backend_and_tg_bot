from fastapi import APIRouter, Body, Depends

from src.utils.dependencies import get_current_user
from src.models.user import User
from src.dao.user import UserDAO
from src.services.payment import PaymentService


router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/webhook")
async def webhook(payment_data = Body(...)):
    print(payment_data)


@router.get("")
async def create_payment(plan_id: int, current_user: User = Depends(get_current_user)):
    payment = await PaymentService.process_payment(plan_id, current_user.id)
    return payment.get("confirmation_url")