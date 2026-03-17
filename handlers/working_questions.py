from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.callbacks_handlers import QuestionConfirm, QuestionSelect
from keyboards.inline import get_confirm_keyboard, get_questions_grid_keyboard
from states.quiz_states import QuizState

router = Router()


@router.callback_query(QuestionSelect.filter())
async def show_question_details(
    callback: CallbackQuery, callback_data: QuestionSelect, state: FSMContext
):
    index = callback_data.index

    data = await state.get_data()
    questions = data.get("questions", [])

    if not questions or index >= len(questions):
        return await callback.answer("Вопрос не найден!", show_alert=True)

    question_text = questions[index].question

    text = f"<b>Вопрос №{index + 1}:</b>\n\n{question_text}\n\nГотов ответить на него?"

    await callback.message.edit_text(
        text, reply_markup=get_confirm_keyboard(index), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(QuestionConfirm.filter(F.action == "no"))
async def return_to_grid(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])

    await callback.message.edit_text(
        "Выбери номер вопроса:",
        reply_markup=get_questions_grid_keyboard(len(questions)),
    )
    await callback.answer()


@router.callback_query(QuestionConfirm.filter(F.action == "yes"))
async def start_answering(
    callback: CallbackQuery, callback_data: QuestionConfirm, state: FSMContext
):
    index = callback_data.index
    questions = (await state.get_data()).get("questions", [])

    await state.update_data(
        current_index=0, chat_history=[], questions=[questions[index]]
    )

    await state.set_state(QuizState.answering_questions)

    await callback.message.edit_text(
        f"Жду твой ответ на вопрос:\n{questions[index].question}. Напиши текстом или запиши голосовое."
    )
    await callback.answer()
