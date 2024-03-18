from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import get_postgresql_url

engine = create_async_engine(get_postgresql_url(), echo=True)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class BaseWithId(DeclarativeBase):
    schema_to_read: type[BaseModel] | None = None
    id: Mapped[int] = mapped_column(primary_key=True)

    def to_read_model(self):
        assert issubclass(self.schema_to_read, BaseModel)
        return self.schema_to_read(**self.__dict__)


class CreatedUpdatedMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
