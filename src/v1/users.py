from typing import Annotated

from fastapi import APIRouter, Depends

from users.schemas import UserSchemaAdd
from users.services import UserService
# from users.services import UserService
from v1.dependencies import UOWDep, user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("")
async def get_users(
    # uow: UOWDep,
    users_service: Annotated[UserService, Depends(user_service)]
):
    # users = await UserService(uow).get_users()
    users = await users_service.get_users()
    return users


@router.post("")
async def add_user(
    user: UserSchemaAdd,
    users_service: Annotated[UserService, Depends(user_service)],
):
    user_id = await users_service.add_user(user)
    return {"user_id": user_id}
