from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.callbacks_handlers import QuestionConfirm, QuestionSelect
from schemas.type_questions import TypeQuestion


menue_category = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 Пройти квиз подряд", callback_data="mode_seq"
            ),
            InlineKeyboardButton(
                text="🔠 Выбрать вопросы из списка", callback_data="mode_grid"
            ),
        ],
    ]
)


async def get_menue(type_questions: list[TypeQuestion]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for type_q in type_questions:
        keyboard.button(text=type_q.name, callback_data=f"category_{type_q.id}")
    return keyboard.as_markup()


def get_confirm_keyboard(index: int):
    """Строит кнопки Да/Нет для конкретного вопроса"""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Да, ответить", callback_data=QuestionConfirm(index=index, action="yes")
    )
    builder.button(
        text="❌ Нет, назад", callback_data=QuestionConfirm(index=index, action="no")
    )

    builder.adjust(2)
    return builder.as_markup()


def get_questions_grid_keyboard(questions_count: int):
    """Строит сетку кнопок 1, 2, 3..."""
    builder = InlineKeyboardBuilder()

    for i in range(questions_count):
        builder.button(text=f"{i + 1}", callback_data=QuestionSelect(index=i))

    builder.adjust(4)
    return builder.as_markup()
