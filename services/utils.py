import asyncio
from io import BytesIO
import logging

from aiogram import Bot
from aiogram.types import Message

from services.deepgram import transcribe_deepgram
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ChatAction
from services.gpt_oss import ask_gpt


async def handle_voice_message(message: Message, bot: Bot) -> str:
    try:
        buffer = BytesIO()
        await bot.download(message.voice, buffer)
        audio_bytes = buffer.getvalue()
        mime_type = message.voice.mime_type or "audio/ogg"
        loop = asyncio.get_running_loop()
        user_answer_text = await loop.run_in_executor(
            None, transcribe_deepgram, audio_bytes, mime_type
        )
        return user_answer_text
    except Exception as e:
        logging.error(f"STT Error: {e}")
        raise Exception("Ошибка при распознавании голоса")


async def handle_text(message: Message, text: str) -> None:
    async with ChatActionSender(
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    ):
        response = await ask_gpt(text)
    logging.info(
        f"Ответ для id = {message.from_user.id}, name = {message.from_user.full_name}, message = {text}, response = {response}"
    )
    await message.reply(response)
