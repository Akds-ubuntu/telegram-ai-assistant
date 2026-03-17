import asyncio
import json
import logging
from typing import Dict
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from contextlib import asynccontextmanager
from config import settings
from aiogram import types
from crud.questions import create_questions
from crud.type_questions import create_question_type
from db.database import get_db
from handlers import (
    answering_questions,
    common,
    follow_up,
    quiz_start,
    working_questions,
)
from loader import bot, dp
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.type_questions import TypeQuestion, TypeQuestionCreate
from fastapi.middleware.cors import CORSMiddleware


WEBHOOK_PATH = "/bot/webhook"
WEBHOOK_URL = f"{settings.DOMEN}{WEBHOOK_PATH}"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Регистрируем роутеры и устанавливаем webhook...")

    dp.include_routers(
        common.router,
        quiz_start.router,
        answering_questions.router,
        follow_up.router,
        working_questions.router,
    )

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

    yield

    logging.info("🚀 Отключаем webhook...")
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://bot.tg-bot-easysobes.duckdns.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request) -> None:
    try:
        logging.info("Received webhook update")
        update = types.Update(**await request.json())
        asyncio.create_task(dp.feed_update(bot, update))
        return Response(status_code=200)
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return Response(status_code=500)


@app.post("/types/{type_id}/questions")
async def load_json_data(
    file: UploadFile, type_id: int, session: AsyncSession = Depends(get_db)
) -> Dict:
    try:
        data = json.loads((await file.read()).decode())
        logging.info(f"type:{type(data)} Received JSONl data: {data}")
        l = await create_questions(session, data, type_id)
        return {"message": "File processed successfully", "count": l}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Failed to process file")


@app.post("/add_type_questions")
async def add_type_questions(
    type_question: TypeQuestionCreate, session: AsyncSession = Depends(get_db)
) -> TypeQuestion:
    return await create_question_type(session, type_question.name)
