import pytest
from factory import Sequence

from tests.integration.users.factories import UserFactory
from users.enums import UserType
from users.schemas import UserSchemaAdd, UserSchema


@pytest.fixture(scope="session")
def add_user_data():
    return UserSchemaAdd(
        first_name="John",
        last_name="Doe",
        email="emai1l@email.com",
        password="password",
        is_active=True,
        user_type=UserType.REGULAR,
    )


@pytest.fixture(scope="session")
def three_random_users() -> list[UserSchema]:
    users = UserFactory.build_batch(3, id=Sequence(lambda n: n))
    return [u.to_read_model() for u in users]
