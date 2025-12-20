import asyncio
import json
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from tg_bot.config import bot, storage, key, TG_ID_ADMIN

def escape_md_v2(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    for ch in escape_chars:
        text = text.replace(ch, f'\\{ch}')
    return text

async def client_message_handler(msg):
    data = json.loads(msg.data.decode())

    if data["type"] == "client.payment.new_subscription":
        text = f"✅ Подписка активированна \n \n> Вы активировали подписку\! \n> \n> Название подписки: {escape_md_v2(data['plan_name'])} \n> \n> Количество устройств в подписке: {data.get('count_devices', 'неизвестно')} \n> \n> Подписка активна до: {escape_md_v2(data['end_date'])} \n> \n> Оплачено: {escape_md_v2(str(data.get('price', 'неизвестно')))} ₽"
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )

    elif data["type"] == "client.payment.update_subscription":
        text = f"✅ Подписка продлена \n \n> Вы продлили подписку\! \n> \n> Название подписки: {escape_md_v2(data['plan_name'])} \n> \n> Количество устройств в подписке: {data.get('count_devices', 'неизвестно')} \n> \n> Подписка активна до: {escape_md_v2(data['end_date'])} \n> \n> Оплачено: {escape_md_v2(str(data.get('price', 'неизвестно')))} ₽"
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )

    elif data["type"] == "client.new.device":
        text = f"✅ Добавлено новое устройство \n \n> Модель устройства: 📲 {escape_md_v2(data['device_model'])} \n> \n> Идентификатор: {escape_md_v2(data['identifier_value'])} \n> \n> Количество подключенных устройства: {data.get('count_devices', 'неизвестно')}/{data.get('max_devices', 'неизвестно')}"
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )

    elif data["type"] == "client.max.devices":
        text = f"🚨 Добавлено максимум устройств \n \n> Вы превысили количество подключенных устройств\! \n> \n> Для увеличения количества устройств перейдите на новый план\! \n> \n> Количество подключенных устройства: {data.get('count_devices', 'неизвестно')}/{data.get('max_devices', 'неизвестно')}"
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )

    elif data["type"] == "client.refferer.new_subscription":
        text = f"🎉 Поздравляем\! \n \n> Для вас активирована новая подписка за приглашенного друга\! \n> \n> Период подписки: {data.get('reward_ref', 'неизвестно')} дней\!"
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )

    elif data["type"] == "client.refferer.update_subscription":
        text = f"🎉 Поздравляем\! \n \n>Вам начислен бонус за приглашенного друга\! \n> \n> Добавили к вашей подписке: {data.get('reward_ref', 'неизвестно')} дней\!"
        print(data["user_id"])
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )
    
    elif data["type"] == "client.referee.new_subscription":
        text = f"Приветсвуем тебя в нашем боте\! \n \n>Вам начислен пригласительный бонус, для вас удвоили пробный период подписки\! \n> \n> Бесплатный период: {int(data.get('reward_ref', 'неизвестно')) * 2} дней\!"
        print(data["user_id"])
        await bot.send_message(
            chat_id=data["user_id"],
            text=text, 
            parse_mode="MarkdownV2"
        )

    elif data["type"] == "client.subscription.expired.notify":
        users: list = data["users_lst_expired"]
        photo = FSInputFile("tg_bot/static/start.jpg")
        for user_id in users:
            try:
                text = "🚨 Ваша подписка закончилась\! \n \n>❌ Подписка закончилась\! \n> \n>✅ Купите подписку, чтобы и дальше пользоваться высокоскоростным и безопасным VPN\! \n> \n>⬇️ Для покупки воспользуйтесь нашим мини приложением\!"
                await bot.send_message(
                    chat_id=user_id,
                    text=text, 
                    parse_mode="MarkdownV2"
                )
            except Exception as e:
                await bot.send_message(chat_id=TG_ID_ADMIN, text=f"❌ Ошибка при отправке сообщений : {e}. Тип: client.subscription.expire.notify")
            await asyncio.sleep(0.05)
        
        for user_id in users:
            try:
                text = (
                    "Привет\! 👋"
                    "\n \n"
                    "Хочу сообщить, что ваша подписка уже завершилась 😕"
                    "\n \n"
                    "Перед тем как вы решите, хотите ли продлить её, мне важно узнать \- вам понравилось пользоваться сервисом\?"
                    "\n \n"
                    "Расскажите, всё ли было удобно и работало так, как вы ожидали\? "
                    "\n \n"
                    "Может, есть моменты, которые хотелось бы улучшить\? "
                    "\n \n"
                    "Мы внимательно читаем каждую обратную связь \- она реально помогает нам развиваться\."
                    "\n \n"
                    "Для обратной связи напишите в поддержку: @sup\_lunovpn 🚀"
                    "\n \n"
                    "Спасибо, что остаетесь с нами 💙"
                )
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=text,
                    parse_mode="MarkdownV2"
                )
            except Exception as e:
                await bot.send_message(chat_id=TG_ID_ADMIN, text=f"❌ Ошибка при отправке сообщений : {e}. Тип: client.subscription.expire.notify")
            await asyncio.sleep(0.05)

    elif data["type"] == "client.subscription.expire.notify":
        users: list = data["users_lst_expire"]
        print(users, "Принял пользователей в тг боте!")
        for user_id in users:
            try:
                text = "🚨 Ваша подписка заканчивается\! \n \n>❌ Подписка завтра закончится\! \n> \n>✅ Продлите подписку, чтобы и дальше пользоваться высокоскоростным и безопасным VPN\! \n> \n>⬇️ Для продления воспользуйтесь нашим мини приложением\!"
                await bot.send_message(
                    chat_id=user_id,
                    text=text, 
                    parse_mode="MarkdownV2"
                )
            except Exception as e:
                await bot.send_message(chat_id=TG_ID_ADMIN, text=f"❌ Ошибка при отправке сообщений : {e}. Тип: client.subscription.expire.notify")
            await asyncio.sleep(0.05)
    

async def request_clients_handler(msg) -> list:
    data = json.loads(msg.data.decode())
    if data["type"] == "request.clients.all":
        users: list = data["users"]
        state = FSMContext(storage=storage, key=key)
        await state.update_data(users=users)
        print(f"✅ {len(users)} пользователей сохранено в FSM!")

    elif data["type"] == "request.clients.not_is_active":
        users: list = data["users"]
        state = FSMContext(storage=storage, key=key)
        await state.update_data(users=users)
        print(f"✅ {len(users)} пользователей с неактивной подпиской сохранено в FSM!")
