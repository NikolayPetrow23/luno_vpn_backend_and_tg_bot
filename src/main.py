from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from src.subscription import router as sub_router
from src.api import router as api_router
from src.admin.view import (
    UsersAdmin, PlansAdmin, SubscriptionsAdmin, PaymentAdmin,
    PaymentTypeAdmin, TrafficAdmin, ShortLinkAdmin, DeviceAdmin,
    ServerAdmin,  HeadersConfigVPNAdmin, PromoCodeAdmin, ReferralAdmin, 
    DeviceIdentifierTypeAdmin, PlanServersAdmin, ConfigurationAdmin
)
from src.admin.auth import authentication_backend
from src.database import engine
from src.tasks.subscription import start_scheduler
from src.broker.nats import nats
from src.broker.client import cb


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await nats.connect("nats://nats:4222")
        await nats.subscribe("app.client.notifications", cb=cb)
    except Exception as e:
        print(f"Ошибка подключения к NATS: {e}")
        raise e
    scheduler = start_scheduler()
    yield
    await nats.close()
    scheduler.shutdown(wait=False)
    

app = FastAPI(
    title="Luno VPN backend",
    version="0.0.1",
    lifespan=lifespan,
    docs_url=None,    # Отключить Swagger UI
    redoc_url=None,   # Отключить ReDoc
    openapi_url=None  # Отключить OpenAPI JSON
)

origins = [
    "http://localhost:3000",
    "http://192.168.0.39:3000",   # адрес твоего фронта
    "http://127.0.0.1:3000",  # если фронт по IP
    "https://lunovpn.tech"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ['http://localhost:5173']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API
app.include_router(api_router)

#Sub
app.include_router(sub_router)

# Панель Админа
admin = Admin(
    app, 
    engine, 
    authentication_backend=authentication_backend
)
admin.add_view(UsersAdmin)
admin.add_view(ReferralAdmin)
admin.add_view(ShortLinkAdmin)
admin.add_view(SubscriptionsAdmin)
admin.add_view(PlansAdmin)
admin.add_view(PromoCodeAdmin)
admin.add_view(PaymentAdmin)
admin.add_view(PaymentTypeAdmin)
admin.add_view(ServerAdmin)
admin.add_view(TrafficAdmin)
admin.add_view(DeviceAdmin)
admin.add_view(HeadersConfigVPNAdmin)
admin.add_view(DeviceIdentifierTypeAdmin)
admin.add_view(PlanServersAdmin)
admin.add_view(ConfigurationAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
