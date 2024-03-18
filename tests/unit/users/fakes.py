from common.repository import AbstractRepository
from common.unitofwork import AbstractUnitOfWork
from users.schemas import UserSchema


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    async def add(self, batch, *args, **kwargs):
        user = UserSchema(**batch, id=1)
        self._batches.add(user)
        return user.id

    async def find_one(self, **filter_by):
        return next(
            b
            for b in self._batches
            if all(
                [False for key, value in filter_by.items() if getattr(key, b) != value]
            )
        )

    async def get_all(self):
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
