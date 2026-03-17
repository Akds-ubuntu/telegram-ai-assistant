from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db.database import session
from crud.questions import get_questions
from keyboards.inline import get_questions_grid_keyboard, menue_category
from states.quiz_states import QuizState
from keyboards.reply import in_progress_keyboard_reply


router = Router()


@router.callback_query(F.data.startswith("category_"))
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split("_")[1]

    async with session() as db:
        questions = await get_questions(db, int(category_id))
    if not questions:
        return await callback.answer(
            "В этой категории пока нет вопросов!", show_alert=True
        )

    await state.update_data(
        questions=questions,
        current_index=0,
        answers=[],
        additional_questions=0,
        chat_history=[],
    )

    await callback.message.edit_text(
        "Категория выбрана! Как хочешь отвечать?", reply_markup=menue_category
    )
    await callback.answer()


@router.callback_query(F.data == "mode_seq")
async def start_sequential_quiz(callback: CallbackQuery, state: FSMContext):
    """РЕЖИМ 1: Подряд"""
    data = await state.get_data()
    questions = data.get("questions", [])

    await state.set_state(QuizState.answering_questions)

    await callback.message.delete()

    await callback.message.answer(
        questions[0].question, reply_markup=in_progress_keyboard_reply
    )
    await callback.answer()


@router.callback_query(F.data == "mode_grid")
async def start_grid_quiz(callback: CallbackQuery, state: FSMContext):
    """РЕЖИМ 2: Сетка вопросов"""
    data = await state.get_data()
    questions = data.get("questions", [])

    await callback.message.edit_text(
        "Выбери номер вопроса:",
        reply_markup=get_questions_grid_keyboard(len(questions)),
    )
    await callback.message.answer(
        "Если хочешь вернуться, нажми кнопку '/start' внизу.",
        reply_markup=in_progress_keyboard_reply,
    )
    await callback.answer()
