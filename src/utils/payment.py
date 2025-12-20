import httpx

from src.config import settings


async def create_payment_platega(
        payment_method: int, 
        amount: int,
        description: str, 
        user_id: int,
        plan_id: int
    ):
    # 2 - СБП, 10 - Банковская карта
    payload = {
        "paymentMethod": payment_method,
        "paymentDetails": {
            "amount": f"{amount:.2f}",
            "currency": "RUB"
        },
        "description": description,
        "return": "https://lunovpn.tech/payment-success",
        "failedUrl": "https://google.com/fail",
        "payload": f"user_id:{user_id}&plan_id:{plan_id}"
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                'Content-Type': 'application/json',
                'X-Secret': settings.config.API_KEY,
                'X-MerchantId': settings.config.MERCHANT_ID
            }
            resp = await client.post(f"https://{settings.config.PLATEGA_URL}/transaction/process", json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
