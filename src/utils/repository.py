from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    async def find_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def find_one(self, **filter_by):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.scalar_one().to_read_model()
            return res
