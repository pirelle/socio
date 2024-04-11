from typing import Annotated

from fastapi import APIRouter, Depends

from users.schemas import UserSchemaAdd, UserSchema
from common.dependencies import UserServiceDep
from v1.utils import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("")
async def get_users(user_service: UserServiceDep):
    users = await user_service.get_users()
    return users


@router.post("", status_code=201)
async def add_user(
    user: UserSchemaAdd,
    user_service: UserServiceDep,
):
    user_id = await user_service.add_user(user)
    return {"user_id": user_id}


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    return current_user
