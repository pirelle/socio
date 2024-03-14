from typing import Annotated

from fastapi import Depends

from users.repositories import UserRepository
from users.services import UserService
from utils.unitofwork import AbstractUnitOfWork, SqlAlchemyUnitOfWork

UOWDep = Annotated[AbstractUnitOfWork, Depends(SqlAlchemyUnitOfWork)]


def user_service():
    return UserService(UserRepository)
