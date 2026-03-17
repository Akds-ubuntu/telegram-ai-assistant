from db.models import TypeQuestionsOrm
from schemas.type_questions import TypeQuestion
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_type_questions(session: AsyncSession) -> list[TypeQuestion]:
    stmt = select(TypeQuestionsOrm)
    result = await session.execute(stmt)
    type_questions_orm = result.scalars().all()
    return [TypeQuestion.model_validate(tq) for tq in type_questions_orm]


async def create_question_type(
    session: AsyncSession, type_question_name: str
) -> TypeQuestion:
    query = select(TypeQuestionsOrm).where(TypeQuestionsOrm.name == type_question_name)
    result = await session.execute(query)

    existing_type = result.scalar_one_or_none()

    if existing_type:
        return {"message": "Type already exists", "id": existing_type.id}

    new_type = TypeQuestionsOrm(name=type_question_name)

    session.add(new_type)
    await session.commit()
    await session.refresh(new_type)

    return TypeQuestion(name=new_type.name, id=new_type.id)
