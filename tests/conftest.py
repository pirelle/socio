
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from fastapi.testclient import TestClient

from common.database import BaseWithId
from common.models import *  # noqa
from common.unitofwork import SqlAlchemyUnitOfWork
from config import get_test_async_postgresql_url, get_test_postgresql_url
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

    async def get_test_uow():
        # async_engine1 = create_async_engine(
        #     get_test_async_postgresql_url(),
        #     # echo=True,
        # )
        # ASession1 = async_sessionmaker()
        # async_connection1 = await async_engine1.connect()
        # async_trans1 = await async_connection1.begin()

        print("going to yield1")

        yield SqlAlchemyUnitOfWork(
            # session_maker=lambda: ASession1(bind=async_connection1, join_transaction_mode="create_savepoint"),
            session_maker=None,
            session=asession,
        )

        # await asession.close()
        print("before trans1 close")
        # await async_trans1.rollback()
        # print("trans1 close")
        # await async_connection1.close()
        # print("connection1 close")

    # app.dependency_overrides[get_uow] = get_test_uow

    print("asession yield")

    yield asession

    await asession.close()
    await async_trans.rollback()
    await async_connection.close()
    print("asession close")


@pytest.fixture(scope="function")
async def client():
    with TestClient(app) as test_client:
        yield test_client
