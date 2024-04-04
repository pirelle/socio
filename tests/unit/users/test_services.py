from unittest.mock import call, Mock

from users.enums import UserType
from users.schemas import UserSchemaAdd
from users.services import UserService
from utils.utils import now


class TestUserService:
    async def test_add_one(self, uow, add_user_data: UserSchemaAdd):
        # "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGVtYWlsLmNvbSJ9.7Lh72XrVoh5YTRN1IrH4ResAmMtk5vL4aKCyMVbaoGc"
        uow.users.add.return_value = 1
        UserService.encrypt_password = Mock(return_value="1")
        user_id = await UserService(uow=uow).add_user(add_user_data)
        assert user_id == 1
        assert uow.users.add.call_args_list == [
            call({
                **add_user_data.model_dump(),
                "password": "1",
            })
        ]
