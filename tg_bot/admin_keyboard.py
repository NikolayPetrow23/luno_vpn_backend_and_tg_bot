from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📣 Рассылка всем"),
            KeyboardButton(text="📢 Рассылка не активным"),
            KeyboardButton(text="🆕 Обновить конфиг на серверах"),
        ]
    ],
    resize_keyboard=True,
)
