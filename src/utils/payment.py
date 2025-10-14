import uuid

from yookassa import Configuration, Payment

from src.config import settings

Configuration.account_id = settings.config.TEST_PAYMENT_SHOP_ID
Configuration.secret_key = settings.config.TEST_PAYMENT_SHOP_TOKEN

async def create_yookassa_payment(amount: int, description: str, user_id: int, plan_id: int):
    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": settings.config.YOOKASSA_RETURN_URL
        },
        "capture": True,
        "description": description,
        "metadata": {
            "user_id": user_id,
            "plan_id": plan_id
        }
    }, uuid.uuid4())

    return {
        "id": payment.id,
        "confirmation_url": payment.confirmation.confirmation_url
    }
