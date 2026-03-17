from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Помощь"), KeyboardButton(text="О боте")]],
    resize_keyboard=True,
)
in_progress_keyboard_reply = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/start")]], resize_keyboard=True
)
