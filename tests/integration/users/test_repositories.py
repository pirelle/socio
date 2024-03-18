from tests.conftest import get_test_session_maker
from users.enums import UserType
from users.schemas import UserSchemaAdd, UserSchema
from common.unitofwork import SqlAlchemyUnitOfWork


class TestUserRepository:
    async def test_one(self, start_end_test_transaction):
        print("run test_one")

    async def test_two(self, start_end_test_transaction):
        print("run test_two")

    async def test_three(self, start_end_test_transaction):
        print("run test_three")

    async def test_add_one(self, start_end_test_transaction):
        # breakpoint()
        uow = SqlAlchemyUnitOfWork(get_test_session_maker())
        print("run test_add_one")
        user = UserSchemaAdd(
            first_name="John",
            last_name="Doe",
            email="emai1l@email.com",
            password="pass",
            is_active=True,
            user_type=UserType.REGULAR,
        )

        async with uow:
            user_id = await uow.users.add_one(user.model_dump())
            await uow.commit()
            created_users = list(await uow.users.find_all())

        expected_user = UserSchema(**user.__dict__, id=user_id)
        assert len(created_users) == 1
        assert expected_user == created_users[0]
