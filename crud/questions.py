import logging

from sqlalchemy import insert, select

from db.models import QuestionsOrm
from schemas.questions import QuestionCreateSchema, QuestionSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def get_questions(session: AsyncSession, type_id: int) -> list[QuestionSchema]:
    stmt = select(QuestionsOrm).where(QuestionsOrm.type_id == type_id)
    result = await session.execute(stmt)
    questions_orm = result.scalars().all()
    return [QuestionSchema.model_validate(q) for q in questions_orm]


async def create_questions(
    session: AsyncSession, questions: list[dict[str, str]], type_id: int
) -> int:
    q_objects = []
    for question in questions:
        q_objects.append(
            QuestionCreateSchema(
                question=question["вопрос"], answer=question["ответ"], type_id=type_id
            )
        )
    logging.info(f"Created QuestionCreateSchema objects: {q_objects}")
    data = [q.model_dump() for q in q_objects]
    stmt = insert(QuestionsOrm).values(data)
    await session.execute(stmt)
    await session.commit()
    return len(data)
