import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient

from common.database import BaseWithId
from common.unitofwork import SqlAlchemyUnitOfWork
from config import get_test_postgresql_url, get_test_async_postgresql_url
from main import app
from common.dependencies import get_uow


@pytest.fixture(scope="session")
async def psql_create_db():
    engine = create_engine(get_test_postgresql_url())

    BaseWithId.metadata.drop_all(engine)
    BaseWithId.metadata.create_all(engine)

    yield engine

    BaseWithId.metadata.drop_all(engine)


@pytest.fixture(scope="function")
async def async_session_maker(psql_create_db):
    async def mm():
        while True:
            ASession = async_sessionmaker()

            async_engine = create_async_engine(
                get_test_async_postgresql_url(),
                # echo=True,
            )
            async_c = await async_engine.connect()
            async_t = await async_c.begin()
            asess = ASession(bind=async_c, join_transaction_mode="create_savepoint")
            yield asess

            await asess.close()
            await async_t.rollback()
            await async_c.close()

            yield 1

    yield mm()


@pytest.fixture(scope="function")
def test_db(async_session_maker):
    def get_test_uow():
        return SqlAlchemyUnitOfWork(session_maker=async_session_maker)

    app.dependency_overrides[get_uow] = get_test_uow
    return async_session_maker


@pytest.fixture(scope="function")
def client(test_db):
    with TestClient(app) as test_client:
        yield test_client
