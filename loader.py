from aiogram import Bot, Dispatcher
from config import settings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
