from datetime import datetime

from tests.unit.users.fakes import FakeUnitOfWork
from users.enums import UserType
from users.schemas import UserSchema, UserSchemaAdd
from users.services import UserService


class TestUserService:
    @classmethod
    def setup_class(cls):
        cls.uow = FakeUnitOfWork()

    async def test_add_one(self):
        user = UserSchemaAdd(
            first_name="John",
            last_name="Doe",
            email="email@email.com",
            password="pass",
            is_active=True,
            user_type=UserType.REGULAR,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_id = await UserService(self.uow).add_user(user)
        assert user_id == 1

        created_users = list(await self.uow.users.get_all())
        assert len(created_users) == 1

        expected_user = UserSchema(**user.__dict__, id=user_id)
        assert expected_user == created_users[0]
