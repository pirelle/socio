from unittest.mock import AsyncMock, Mock

import pytest

from common.unitofwork import AbstractUnitOfWork
from main import app
from fastapi.testclient import TestClient

from posts.repositories import PostRepository
from users.repositories import UserRepository
from users.services import UserService
from v1.dependencies import get_user_service


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def user_service() -> AsyncMock:
    mocked_user_service = AsyncMock(spec=UserService)
    app.dependency_overrides[get_user_service] = lambda: mocked_user_service
    return mocked_user_service


@pytest.fixture(scope="function")
def uow() -> AsyncMock:
    mocked_uow = AsyncMock(spec=AbstractUnitOfWork)
    mocked_uow.users = AsyncMock(spec=UserRepository)
    mocked_uow.posts = AsyncMock(spec=PostRepository)
    return mocked_uow
