from typing import Annotated

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Model


intpk = Annotated[int, mapped_column(primary_key=True)]


class TypeQuestionsOrm(Model):
    __tablename__ = "type_questions"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class QuestionsOrm(Model):
    __tablename__ = "questions"

    id: Mapped[intpk]
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    type_id: Mapped[int] = mapped_column(
        ForeignKey("type_questions.id", ondelete="CASCADE"), nullable=False
    )
