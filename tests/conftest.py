import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from config import get_test_postgresql_url, get_test_async_postgresql_url
from common.database import BaseWithId
from common.models import *  # noqa


def get_test_session_maker():
    async_engine = create_async_engine(
        get_test_async_postgresql_url(),
        echo=True,
    )
    async_session_maker = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return async_session_maker


@pytest.fixture(scope="session")
async def psql_create_db():
    engine = create_engine(get_test_postgresql_url())
    BaseWithId.metadata.create_all(engine)
    yield None
    BaseWithId.metadata.drop_all(engine)


@pytest.fixture(scope="function")
async def start_end_test_transaction(psql_create_db):
    async_session = get_test_session_maker()()
    async with async_session.begin():
        yield None
    await async_session.rollback()
