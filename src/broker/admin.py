import datetime
import json

from src.broker.nats import nats


async def push_exception_admin(
    user_id: int | None, 
    exception: Exception | None,
    path: str,
    raise_exc: str
) -> None:
    payload = {
        "type": "error.admin.notification",
        "user_id": user_id,
        "exception": str(exception),
        "raise_exc": raise_exc,
        "path": path,
        "timestamp": str(datetime.datetime.now())
    }
    await nats.publish(
        "bot.admin.notifications", 
        json.dumps(payload).encode()
    )
