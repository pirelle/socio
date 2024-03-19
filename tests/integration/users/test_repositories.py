
from sqlalchemy.ext.asyncio import AsyncSession

from tests.integration.users.factories import UserFactory
from users.enums import UserType
from users.repositories import UserRepository
from users.schemas import UserSchema, UserSchemaAdd


class TestUserRepository:
    async def test_add(self, async_session: AsyncSession):
        user = UserSchemaAdd(
            first_name="John",
            last_name="Doe",
            email="emai1l@email.com",
            password="pass",
            is_active=True,
            user_type=UserType.REGULAR,
        )
        user_repo = UserRepository(async_session)
        user_id = await user_repo.add(user.model_dump())
        await async_session.commit()
        created_users = list(await user_repo.get_all())

        expected_user = UserSchema(**user.__dict__, id=user_id)
        assert len(created_users) == 1
        assert expected_user == created_users[0]

    async def test_filter(self, async_session: AsyncSession):
        UserFactory.create_batch(
            3, user_type=UserType.REGULAR, session=async_session.sync_session
        )
        UserFactory.create_batch(
            3, user_type=UserType.MODERATOR, session=async_session.sync_session
        )
        user_repo = UserRepository(async_session)
        created_users = await user_repo.get_all()
        assert len(created_users) == 6

    async def test_with_followers(self, async_session: AsyncSession):
        users = UserFactory.build_batch(
            3, user_type=UserType.REGULAR
        )
        async_session.add_all(users)
        await async_session.commit()
        user_repo = UserRepository(async_session)
        created_users = await user_repo.get_all()


        created_users = await user_repo.get_with_followers(user_id=created_users[0].id)
        assert len(created_users) == 6
