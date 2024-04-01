from typing import Annotated

from fastapi import Depends

from common.database import async_session_maker
from common.unitofwork import AbstractUnitOfWork, SqlAlchemyUnitOfWork


def get_uow():
    yield SqlAlchemyUnitOfWork(session_maker=async_session_maker)


UOWDep = Annotated[
    AbstractUnitOfWork,
    Depends(get_uow),
]
