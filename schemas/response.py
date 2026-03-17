from pydantic import BaseModel, Field


class QuizResponse(BaseModel):
    is_correct: bool = Field(
        description="True если ответ правильный и к нему нельзя придраться, иначе если ответ имеет неоднозначность и можно задать уточняющие вопросы то тогда False"
    )
    reply_text: str = Field(description="Ответ пользователю в стиле интервьювера")
