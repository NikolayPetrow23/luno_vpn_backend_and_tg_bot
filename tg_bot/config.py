import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import StorageKey
from nats.aio.client import Client as NATS

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

TG_ID_ADMIN = int(os.getenv("TG_ID_ADMIN", "0"))

WEB_SERVER_HOST = "127.0.0.1"

WEB_SERVER_PORT = 8080

WEBHOOK_PATH = "/"

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")

bot = Bot(TOKEN)
nats_client = NATS()
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
key = StorageKey(
    bot_id=bot.id,
    chat_id=TG_ID_ADMIN,
    user_id=TG_ID_ADMIN
)
