from datetime import datetime

from users.enums import UserType
from users.schemas import UserSchemaAdd, UserSchema
from users.services import UserService
from utils.repository import AbstractRepository
from utils.unitofwork import AbstractUnitOfWork


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    async def add_one(self, batch, *args, **kwargs):
        user = UserSchema(**batch, id=1)
        self._batches.add(user)
        return user.id

    async def find_one(self, **filter_by):
        return next(
            b
            for b in self._batches
            if all([
                False
                for key, value in filter_by.items()
                if getattr(key, b) != value
            ])
        )

    async def find_all(self):
        return self._batches


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.commited = False

    async def __aenter__(self):
        self.users = FakeRepository([])

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        self.commited = True

    async def rollback(self):
        pass

class TestUserService:
    @classmethod
    def setup_class(cls):
        cls.uow = FakeUnitOfWork()

    async def test_add_one(self):
        user = UserSchemaAdd(
            first_name="John",
            last_name="Doe",
            email="<EMAIL>",
            password="pass",
            is_active=True,
            user_type=UserType.REGULAR,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_id = await UserService(self.uow).add_user(user)
        assert user_id == 1

        created_users = list(await self.uow.users.find_all())
        assert len(created_users) == 1

        expected_user = UserSchema(**user.__dict__, id=user_id)
        assert expected_user == created_users[0]
