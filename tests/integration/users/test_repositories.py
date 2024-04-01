from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from posts.models import Post, Comment
from tests.integration.users.factories import UserFactory
from users.enums import UserType
from users.models import Follower
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
        users = UserFactory.build_batch(3, user_type=UserType.REGULAR)
        users += UserFactory.build_batch(3, user_type=UserType.MODERATOR)
        async_session.add_all(users)
        await async_session.commit()

        user_repo = UserRepository(async_session)
        created_users = await user_repo.get_all()
        assert len(created_users) == 6

        filtered_users = await user_repo.filter(user_type=UserType.REGULAR)
        assert len(filtered_users) == 3
        assert {UserType.REGULAR} == {user.user_type for user in filtered_users}

    async def test_with_followers(self, async_session: AsyncSession):
        users = UserFactory.build_batch(4)
        async_session.add_all(users)
        await async_session.commit()

        user_repo = UserRepository(async_session)
        users = await user_repo.get_all()

        user1, user2, user3, user4 = users
        await async_session.execute(
            insert(Follower).values(follower_id=user2.id, following_id=user1.id)
        )
        await async_session.execute(
            insert(Follower).values(follower_id=user3.id, following_id=user1.id)
        )
        await async_session.execute(
            insert(Follower).values(follower_id=user4.id, following_id=user2.id)
        )
        await async_session.execute(
            insert(Post).values(
                user_id=user1.id,
                text="text 1",
            )
        )
        await async_session.execute(
            insert(Post).values(
                user_id=user1.id,
                text="text 2",
            )
        )
        await async_session.execute(
            insert(Post).values(
                user_id=user2.id,
                text="text 3",
            )
        )
        await async_session.execute(
            insert(Comment).values(post_id=1, user_id=user2.id, text="comment 1")
        )
        await async_session.execute(
            insert(Comment).values(post_id=1, user_id=user3.id, text="comment 2")
        )
        await async_session.commit()

        user, followers, posts = await user_repo.get_with_initial_info(
            user_id=users[0].id
        )
        # breakpoint()
        # assert len(created_users) == 6
