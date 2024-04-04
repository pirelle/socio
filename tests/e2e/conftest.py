import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient

from common.database import BaseWithId
from config import get_test_postgresql_url, get_test_async_postgresql_url
from main import app


@pytest.fixture(scope="session")
async def psql_create_db():
    engine = create_engine(get_test_postgresql_url())

    BaseWithId.metadata.drop_all(engine)
    BaseWithId.metadata.create_all(engine)

    yield engine

    BaseWithId.metadata.drop_all(engine)


@pytest.fixture(scope="function")
async def async_session(psql_create_db):
    async_engine = create_async_engine(
        get_test_async_postgresql_url(),
        # echo=True,
    )
    ASession = async_sessionmaker()
    async_connection = await async_engine.connect()
    async_trans = await async_connection.begin()
    asession = ASession(bind=async_connection, join_transaction_mode="create_savepoint")

    yield asession

    await asession.close()
    await async_trans.rollback()
    await async_connection.close()

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client
