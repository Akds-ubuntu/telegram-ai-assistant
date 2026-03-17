import logging
from aiogram.fsm.context import FSMContext

from aiogram import F, Bot, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from requests import session

from crud.type_questions import get_type_questions
from keyboards.inline import get_menue
from services.lang_gpt_oss import evaluate_answer
from services.utils import handle_voice_message
from states.quiz_states import QuizState
from langchain_core.messages import HumanMessage, AIMessage


router = Router()


@router.message(StateFilter(QuizState.answering_questions), F.text | F.voice)
async def process_quiz_answer(message: Message, state: FSMContext, bot: Bot):
    user_answer_text = ""

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

    data = await state.get_data()
    questions = data["questions"]
    current_index = data["current_index"]
    answers = data.get("answers", [])
    chat_history = data.get("chat_history", [])

    answers.append(user_answer_text)
    llm_response = await evaluate_answer(
        questions[current_index].question,
        questions[current_index].answer,
        user_answer_text,
        chat_history,
    )
    if llm_response.is_correct:
        await message.answer(f"{llm_response.reply_text}")
        current_index += 1
        if current_index < len(questions):
            await state.update_data(current_index=current_index, answers=answers)
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
        await state.set_state(QuizState.follow_up)
        history = [
            HumanMessage(content=user_answer_text),
            AIMessage(content=llm_response.reply_text),
        ]
        await state.update_data(
            chat_history=history,
            additional_questions=data.get("additional_questions", 0) + 1,
        )
        await message.answer(f"Доп вопрос:{llm_response.reply_text}")
