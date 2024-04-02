from unittest.mock import AsyncMock, Mock

import pytest

from common.unitofwork import SqlAlchemyUnitOfWork
from main import app
from users.enums import UserType
from users.repositories import UserRepository
from users.schemas import UserSchema


@pytest.fixture(scope="function")
async def uow_mock():
    uow_mocked = AsyncMock(spec=SqlAlchemyUnitOfWork)
    with app.container.uow.override(uow_mocked):
        yield uow_mocked


@pytest.fixture(scope="function")
async def users(uow_mock):
    users_list = [
        UserSchema(
            id=1,
            first_name="",
            last_name="",
            email="test@email.com",
            password="$2b$12$IHRIA3SVdclsOsUSsf6UbeRjfX8LoVYXJwlmA8p2SESv4i3eQSQ7m",
            is_active=True,
            user_type=UserType.REGULAR,
        )
    ]
    uow_mock.users = Mock(spec=UserRepository)
    uow_mock.users.get_all.return_value = users_list
    uow_mock.users.get.return_value = users_list[0]
    yield users_list
