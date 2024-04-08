from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from users.schemas import UserSchemaAdd
from common.dependencies import UserServiceDep

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


class Token(BaseModel):
    access_token: str
    token_type: str


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


@router.post("/token")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=404, detail="User with these credentials not found"
        )
    access_token = user_service.create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
