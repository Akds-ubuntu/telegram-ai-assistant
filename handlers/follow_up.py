import logging

from aiogram import F, Bot, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from db.database import session
from crud.type_questions import get_type_questions
from keyboards.inline import get_menue
from services.lang_gpt_oss import evaluate_answer
from services.utils import handle_voice_message
from states.quiz_states import QuizState
from aiogram.fsm.context import FSMContext
from langchain_core.messages import HumanMessage, AIMessage


router = Router()


@router.message(StateFilter(QuizState.follow_up), F.text | F.voice)
async def process_follow_up(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    questions = data["questions"]
    q_text = data["questions"]
    current_index = data["current_index"]
    correct = q_text[current_index].answer
    history = data.get("chat_history", [])
    additional_questions = data.get("additional_questions")
    if message.voice:
        processing_msg = await message.answer("⏳ Распознаю твой ответ...")
        try:
            user_answer_text = await handle_voice_message(message, bot)
            await processing_msg.delete()

            if not user_answer_text.strip():
                await message.answer(
                    "Не удалось распознать речь. Попробуй еще раз или напиши текстом."
                )
                return

            await message.reply(f"📝 Твой ответ (распознано):\n{user_answer_text}")
        except Exception as e:
            await processing_msg.delete()
            logging.exception(f"Ошибка при распознавании ответа: {e}")
            await message.answer(
                "Произошла ошибка при распознавании. Напиши текстом, пожалуйста."
            )
            return
    else:
        user_answer_text = message.text
    response = await evaluate_answer(q_text, correct, user_answer_text, history=history)
    if response.is_correct:
        await message.answer(
            "🧐 Ладно, на этот раз выкрутился. Слушай следующий вопрос."
        )

        await state.update_data(chat_history=[])
        await state.set_state(QuizState.answering_questions)
        current_index += 1
        if current_index < len(questions):
            await state.update_data(current_index=current_index)
            await message.answer(questions[current_index].question)

        else:
            await message.answer(
                "Спасибо! Твои ответы приняты. Обрабатываю результаты..."
            )

            await state.clear()

            async with session() as db:
                type_questions = await get_type_questions(db)
            await message.answer(
                "Выбери категорию вопросов:",
                reply_markup=await get_menue(type_questions),
            )
    else:
        additional_questions += 1
        if data.get("additional_questions", 0) >= 3:
            await message.answer(
                "Похоже, ты не хочешь отвечать на вопрос. Пойдем дальше."
            )
            await state.update_data(chat_history=[])
            await state.set_state(QuizState.answering_questions)
            current_index += 1
            if current_index < len(questions):
                await state.update_data(
                    current_index=current_index, additional_questions=0
                )
                await message.answer(questions[current_index].question)
            else:
                await message.answer(
                    "Спасибо! Твои ответы приняты. Обрабатываю результаты..."
                )

                await state.clear()

                async with session() as db:
                    type_questions = await get_type_questions(db)
                await message.answer(
                    "Выбери категорию вопросов:",
                    reply_markup=await get_menue(type_questions),
                )
        else:
            history.append(HumanMessage(content=user_answer_text))
            history.append(AIMessage(content=response.reply_text))
            await state.update_data(
                chat_history=history, additional_questions=additional_questions
            )

            await message.answer(response.reply_text)
