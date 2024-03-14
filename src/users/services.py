from users.schemas import UserSchemaAdd, UserSchema
from utils.repository import AbstractRepository, SQLAlchemyRepository
from utils.unitofwork import AbstractUnitOfWork


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserSchemaAdd) -> int:
        user_dict = user.model_dump()
        async with self.uow:
            user_id = await self.uow.users.add_one(user_dict)
            await self.uow.commit()
            return user_id

    async def get_users(self) -> [UserSchema]:
        async with self.uow:
            users = await self.uow.users.find_all()
            return users

# class UserService:
#     def __init__(self, users_repo: type[AbstractRepository]):
#         self.users_repo: AbstractRepository = users_repo()
#
#     async def add_user(self, user: UserSchemaAdd):
#         user_dict = user.model_dump()
#         user_id = await self.users_repo.add_one(user_dict)
#         return user_id
#
#     async def get_users(self):
#         users = await self.users_repo.find_all()
#         return users
