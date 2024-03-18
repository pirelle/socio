from common.unitofwork import AbstractUnitOfWork
from users.schemas import UserSchema, UserSchemaAdd


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserSchemaAdd) -> int:
        user_dict = user.model_dump()
        async with self.uow:
            user_id = await self.uow.users.add(user_dict)
            await self.uow.commit()
            return user_id

    async def get_users(self) -> list[UserSchema]:
        async with self.uow:
            users = await self.uow.users.get_all()
            return users
