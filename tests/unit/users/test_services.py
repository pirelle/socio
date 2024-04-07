from unittest.mock import call

import pytest
from passlib.exc import UnknownHashError

from users.containers import Container as UserContainer
from users.schemas import UserSchemaAdd


container = UserContainer()


async def test_add_one(uow, add_user_data: UserSchemaAdd):
    uow.users.add.return_value = 1

    user_service = container.user_service(
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


async def test_encrypt_verify_password(uow):
    password = "password"

    user_service = container.user_service(uow=uow)

    encrypted_password = user_service.encrypt_password(password)
    assert password != encrypted_password
    assert user_service.verify_password(password, encrypted_password)
    with pytest.raises(UnknownHashError):
        user_service.verify_password(password, password)


async def test_get_users(uow): ...
