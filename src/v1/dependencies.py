from typing import Annotated

from fastapi import Depends

from common.database import async_session_maker
from common.unitofwork import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from users.services import UserService


def get_uow():
    return SqlAlchemyUnitOfWork(session_maker=async_session_maker)


UOWDep = Annotated[
    AbstractUnitOfWork,
    Depends(get_uow),
]


def get_user_service(uow: UOWDep):
    return UserService(uow=uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
