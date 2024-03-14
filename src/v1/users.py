from typing import Annotated

from fastapi import APIRouter, Depends

from users.schemas import UserSchemaAdd
from users.services import UserService
from v1.dependencies import UOWDep, user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("")
async def get_users(
    uow: UOWDep,
):
    users = await UserService(uow).get_users()
    return users


@router.post("")
async def add_user(
    user: UserSchemaAdd,
    uow: UOWDep,
):
    user_id = await UserService(uow).add_user(user)
    return {"user_id": user_id}
