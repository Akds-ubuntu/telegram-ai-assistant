from aiogram.fsm.state import State, StatesGroup


class QuizState(StatesGroup):
    answering_questions = State()
    follow_up = State()
