from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(settings.DATABASE_URL, echo=True)

session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with session() as db:
        yield db


class Model(DeclarativeBase):
    pass
