import json
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

from tg_bot.config import TG_ID_ADMIN
from tg_bot.admin_keyboard import keyboard
from tg_bot.config import nats_client

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:  
    chat_id = message.chat.id
    text = message.text or ""
    parts = text.split(maxsplit=1)
    ref_code = parts[1] if len(parts) > 1 else None
    if ref_code: 
        payload = {
            "type": "app.client.reffer.start",
            "ref_code": ref_code,
            "user_telegram_id": chat_id,
            "user_username": message.from_user.username or "",
            "first_name": message.from_user.first_name or ""
            
        }
        await nats_client.publish("app.client.notifications", json.dumps(payload).encode())
    else:
        payload = {
            "type": "app.client.create",
            "user_telegram_id": chat_id,
            "user_username": message.from_user.username or "",
            "first_name": message.from_user.first_name or ""
        }
        await nats_client.publish("app.client.notifications", json.dumps(payload).encode())
    if chat_id == TG_ID_ADMIN:
        await message.answer(
            text=f"Добро пожаловать, администратор! Вы можете использовать панель управления нижe",
            reply_markup=keyboard
        )
    else:
        photo = FSInputFile("tg_bot/static/start.jpg")
        await message.answer_photo(
            photo=photo,  # или file_id, или путь к файлу
            caption=f"Вот твоя картинка 📸 \n Твой payload: {payload}"
        )


class BroadcastState(StatesGroup):
    waiting_for_text = State()
    waiting_for_photo = State()


@router.message(F.text == "📢 Рассылка всем")
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != TG_ID_ADMIN:
        return await message.answer("🚫 У вас нет доступа.")
    
    await message.answer("📸 Отправь картинку для рассылки:")
    payload = {
        "type": "app.clients.get.all",
    }    
    await nats_client.publish("app.client.notifications", json.dumps(payload).encode())
    await state.set_state(BroadcastState.waiting_for_photo)


@router.message(BroadcastState.waiting_for_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id  # берём последнее фото (наилучшее качество)
    await state.update_data(photo_id=photo)
    await message.answer("✍️ Теперь отправь текст для рассылки:")
    await state.set_state(BroadcastState.waiting_for_text)


@router.message(BroadcastState.waiting_for_text)
async def handle_text(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = data["photo_id"]
    text = message.text

    await message.answer("🚀 Рассылка началась...")

    data = await state.get_data()
    users = data.get("users") or []
    sent = 0

    for uid in users:
        try:
            await message.bot.send_photo(
                chat_id=uid,
                photo=photo_id,
                caption=text
            )
            sent += 1
        except Exception as e:
            await message.answer(f"❌ Ошибка при отправке {uid}: {e}")
        await asyncio.sleep(0.05)

    await message.answer(f"✅ Рассылка завершена! Отправлено {sent} сообщений.")
    await state.clear()


@router.message(F.text == "📢 Рассылка не активным")
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != TG_ID_ADMIN:
        return await message.answer("🚫 У вас нет доступа.")
    
    await message.answer("📸 Отправь картинку для рассылки:")
    payload = {
        "type": "app.clients.get.not_is_active",
    }    
    await nats_client.publish("app.client.notifications", json.dumps(payload).encode())
    await state.set_state(BroadcastState.waiting_for_photo)


@router.message(BroadcastState.waiting_for_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id  # берём последнее фото (наилучшее качество)
    await state.update_data(photo_id=photo)
    await message.answer("✍️ Теперь отправь текст для рассылки:")
    await state.set_state(BroadcastState.waiting_for_text)


@router.message(BroadcastState.waiting_for_text)
async def handle_text(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = data["photo_id"]
    text = message.text

    await message.answer("🚀 Рассылка началась...")

    data = await state.get_data()
    users = data.get("users") or []
    sent = 0

    for uid in users:
        try:
            await message.bot.send_photo(
                chat_id=uid,
                photo=photo_id,
                caption=text
            )
            sent += 1
        except Exception as e:
            await message.answer(f"❌ Ошибка при отправке {uid}: {e}")
        await asyncio.sleep(0.05)

    await message.answer(f"✅ Рассылка завершена! Отправлено {sent} сообщений.")
    await state.clear()


@router.message(F.text == "🆕 Обновить конфиг на серверах")
async def start_broadcast(message: Message):
    if message.from_user.id != TG_ID_ADMIN:
        return await message.answer("🚫 У вас нет доступа.")
    
    try:
        payload = {
            "type": "app.servers.update.config",
        }
        await nats_client.publish("app.client.notifications", json.dumps(payload).encode())
        await message.answer("Все отлично 🚀 Конфиги на серверах обновляются!")
    except Exception as e:
        await message.answer(f"❌ Ошибка при обновлении конфигов на серверах: {e}")