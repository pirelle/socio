from unittest.mock import AsyncMock, Mock

import pytest
from starlette.testclient import TestClient

from common.unitofwork import SqlAlchemyUnitOfWork
from main import app
from users.enums import UserType
from users.repositories import UserRepository
from users.schemas import UserSchema


@pytest.fixture(scope='function')
async def uow_mock():
    uow_mocked = AsyncMock(spec=SqlAlchemyUnitOfWork)
    with app.container.uow.override(uow_mocked):
        yield uow_mocked

@pytest.fixture(scope='function')
async def users(uow_mock):
    users_list = [
        UserSchema(
            id=1,
            first_name="",
            last_name="",
            email="asdf@asdf.ff",
            password="str",
            is_active=True,
            user_type=UserType.REGULAR
        )
    ]
    uow_mock.users = Mock(spec=UserRepository)
    uow_mock.users.get_all.return_value = users_list
    yield users_list
