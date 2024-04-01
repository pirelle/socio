from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from users.schemas import UserSchemaAdd
from users.services import UserService, create_access_token, SyncUserService
from users.containers import Container as UserContainer
from v1.dependencies import UOWDep

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


class Token(BaseModel):
    access_token: str
    token_type: str


@router.get("")
@inject
async def get_users(
    user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    users = await user_service.get_users()
    return users


@router.get("/sync")
@inject
async def get_users_sync(
    user_service: SyncUserService = Depends(Provide[UserContainer.sync_user_service]),
):
    users = user_service.get_users()
    return users


@router.post("")
async def add_user(
    user: UserSchemaAdd,
    uow: UOWDep,
    user_service: Annotated[UserService, Depends(UserService)],
):
    user_id = await user_service.add_user(uow, user)
    return {"user_id": user_id}


@router.post("/token")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UOWDep,
    user_service: Annotated[UserService, Depends(UserService)],
):
    user = await user_service.authenticate_user(
        uow, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=404, detail="User with these credentials not found"
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
