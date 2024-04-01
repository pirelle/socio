import json
from unittest.mock import Mock, AsyncMock

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from common.unitofwork import SqlAlchemyUnitOfWork
from main import app
from tests.integration.users.factories import UserFactory
from users.enums import UserType
from users.repositories import UserRepository
from users.schemas import UserSchema


class TestApi:
    async def test_users(self, client, users):
        print(1)
        # client = TestClient(app=app)
        # uow_mock = AsyncMock(spec=SqlAlchemyUnitOfWork)

        # with app.container.uow.override(uow_mock):
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == [json.loads(users[0].model_dump_json())]

    async def test_token_no_user(self):
        print(2)
        client = TestClient(app=app)
        response = client.post("/users/token", data={"username": "1", "password": "2"})
        assert response.status_code == 404
        assert response.json() == {'detail': 'User with these credentials not found'}

    async def test_token_wrong_password(self, async_session: AsyncSession):
        print(3)

        user = UserFactory.build(
            email="test@email.com",
            password="$2b$12$IHRIA3SVdclsOsUSsf6UbeRjfX8LoVYXJwlmA8p2SESv4i3eQSQ7m",
        )
        async_session.add(user)
        await async_session.commit()

        client = TestClient(app=app)
        response = client.post("/users/token", data={"username": "test@email.com", "password": "2"})
        assert response.status_code == 404
        assert response.json() == {'detail': 'User with these credentials not found'}

    async def test_token(self):
        client = TestClient(app=app)
        response = client.post("/users/token", data={"username": "test@email.com", "password": "password"})
        assert response.status_code == 404
        assert response.json() == {'detail': 'User with these credentials not found'}
