from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import BaseWithId


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: type[BaseWithId] | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict):
        assert self.model is not None
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def get(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        try:
            res = res.scalar_one().to_read_model()
        except NoResultFound:
            res = None
        return res

    async def filter(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return [row[0].to_read_model() for row in res.all()]
