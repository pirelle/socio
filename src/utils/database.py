from datetime import datetime

from sqlalchemy import DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase

from config import get_postgresql_url

engine = create_async_engine(get_postgresql_url(), echo=True)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
session_maker = sessionmaker(
    bind=create_engine(
        get_postgresql_url(),
    )
)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


def get_session():
    with session_maker() as session:
        yield session


class Base(DeclarativeBase):

    def to_read_model(self):
        from users.schemas import UserSchema
        return UserSchema(**self.__dict__)



class CreatedUpdatedMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=func.current_timestamp())
