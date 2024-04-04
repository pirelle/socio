import pytest

from users.enums import UserType
from users.schemas import UserSchemaAdd


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
