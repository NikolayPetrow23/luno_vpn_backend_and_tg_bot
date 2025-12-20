import json

from tg_bot.config import TG_ID_ADMIN, bot


def escape_md_v2(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    for ch in escape_chars:
        text = text.replace(ch, f'\\{ch}')
    return text


async def admin_message_handler(msg):
    data = json.loads(msg.data.decode())
    if data["type"] == "server.status.ok":
        text = f"✅ Серверы в порядке ✅ \n \n {data['result'].get('xray_test','нет данных')} \n \n Данные о скорости: {data['result'].get('speed_test','нет данных')}"
        await bot.send_message(
            chat_id=TG_ID_ADMIN,
            text=text, 
        )
    elif data["type"] == "server.status.error":
        text = f"‼️ Ошибка при проверки серверов ‼️ \n \n> Сервер {escape_md_v2(data['server'])} упал ❌ \n> \n> Ошибка при проверки сервера: {escape_md_v2(data['error'])}"
        await bot.send_message(
            chat_id=TG_ID_ADMIN,
            text=text,
            parse_mode="MarkdownV2"
        )
    elif data["type"] == "error.admin.notification":
        text = f"⚠️ Ошибка ⚠️ \n \n> Пользователь: {data['user_id']} \n> Путь: {escape_md_v2(data['path'])} \n> Вызываемое исключение: {escape_md_v2(data['raise_exc'])} \n> Ошибка: {escape_md_v2(data['exception'])} \n> Время: {escape_md_v2(data['timestamp'])}"
        await bot.send_message(
            chat_id=TG_ID_ADMIN,
            text=text,
            parse_mode="MarkdownV2"
        )
