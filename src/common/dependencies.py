from typing import Annotated

from fastapi import Depends


from users.services import UserService
from users.containers import Container as UserContainer


user_container = UserContainer()


async def get_user_service():
    user_service = await user_container.user_service()
    return user_service


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
