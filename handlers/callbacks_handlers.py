from aiogram.filters.callback_data import CallbackData


# Колбэк для выбора вопроса из списка
class QuestionSelect(CallbackData, prefix="q_sel"):
    index: int  # Индекс  из БД)


# Колбэк для кнопок "Да/Нет"
class QuestionConfirm(CallbackData, prefix="q_conf"):
    index: int
    action: str  # "yes" или "no"
