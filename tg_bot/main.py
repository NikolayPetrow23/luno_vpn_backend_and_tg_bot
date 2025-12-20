import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import sys


sys.path.append('')

from tg_bot import config
from tg_bot.router import router as general_router
from tg_bot.config import bot, nats_client, dp
from tg_bot.admin import admin_message_handler
from tg_bot.client import client_message_handler, request_clients_handler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def nats_listener():
    """Слушатель NATS — принимает сообщения и шлёт их пользователю."""
    await nats_client.connect("nats://nats:4222")
    logging.info("🤖 Connected to NATS from bot")

    await nats_client.subscribe("bot.admin.notifications", cb=admin_message_handler)
    await nats_client.subscribe("bot.client.notifications", cb=client_message_handler)
    await nats_client.subscribe("bot.request.clients", cb=request_clients_handler)
    logging.info("🔔 Subscribed to bot.notifications")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}", 
        secret_token=config.WEBHOOK_SECRET
    )
    asyncio.create_task(nats_listener())
    logging.info("🚀 Bot startup completed (webhook + NATS listener started)")


async def on_shutdown(app: web.Application):
    """Закрываем соединения при остановке"""
    if nats_client.is_connected:
        await nats_client.close()
    await bot.session.close()
    logging.info("🛑 Shutdown complete")


def main(dp: Dispatcher) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )

    dp.include_routers(general_router)

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.WEBHOOK_SECRET,
    )

    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(dp=dp)