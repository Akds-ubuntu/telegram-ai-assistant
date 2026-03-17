import asyncio
import logging
from loader import bot, dp
from handlers import (
    answering_questions,
    follow_up,
    quiz_start,
    common,
    working_questions,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def start_polling() -> None:
    try:
        dp.include_routers(
            common.router,
            quiz_start.router,
            answering_questions.router,
            follow_up.router,
            working_questions.router,
        )
        logging.info("🚀 Бот запущен на polling'е...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка при запуске polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start_polling())
