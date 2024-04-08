from unittest.mock import call

import pytest
from passlib.exc import UnknownHashError

from users.containers import Container as UserContainer
from users.schemas import UserSchemaAdd


class TestUserService:
    @classmethod
    def setup_class(cls):
        cls.container = UserContainer()
        cls.password = "password"
        cls.incorrect_password = "password1"
        cls.password_hash = (
            "$2b$12$Y/OMk0d.6SrFaUegjauehujZa2DUk8qofnepoY.ZpTED88awc07FC"
        )

    async def test_add_one(self, uow, add_user_data: UserSchemaAdd):
        uow.users.add.return_value = 1

        user_service = self.container.user_service(
            uow=uow, encrypt_password_strat=lambda password: "1"
        )
        user_id = await user_service.add_user(add_user_data)
        assert user_id == 1
        assert uow.users.add.call_args_list == [
            call(
                {
                    **add_user_data.model_dump(),
                    "password": "1",
                }
            )
        ]

    async def test_encrypt_verify_password(self, uow):
        user_service = self.container.user_service(uow=uow)

        encrypted_password = user_service.encrypt_password(self.password)
        assert self.password != encrypted_password
        assert user_service.verify_password(self.password, encrypted_password)

        with pytest.raises(UnknownHashError):
            user_service.verify_password(self.password, self.password)

    async def test_get_users(self, uow, three_random_users):
        uow.users.get_all.return_value = three_random_users

        user_service = self.container.user_service(
            uow=uow, encrypt_password_strat=lambda password: "1"
        )
        assert (await user_service.get_users()) == three_random_users

    async def test_authenticate_user(self, uow, three_random_users):
        user = three_random_users[0]
        user.password = self.password_hash
        uow.users.get.return_value = user
        user_service = self.container.user_service(uow=uow)

        # correct username and password
        is_authenticated = await user_service.authenticate_user(
            user.email,
            self.password,
        )
        assert is_authenticated == user
        assert uow.users.get.call_args_list == [call(email=user.email)]

        # check incorrect password
        is_authenticated = await user_service.authenticate_user(
            user.email,
            self.incorrect_password,
        )
        assert is_authenticated is None

        # check incorrect username (user doesn't exist)
        uow.users.get.return_value = None
        is_authenticated = await user_service.authenticate_user(
            user.email,
            self.password,
        )
        assert is_authenticated is None
