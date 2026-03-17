from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from aiogram import html
from crud.type_questions import get_type_questions
from keyboards.inline import get_menue
from db.database import session


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    async with session() as db:
        type_questions = await get_type_questions(db)

    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\nПожалуйста, выбери категорию вопросов ниже:",
        reply_markup=await get_menue(type_questions),
    )
