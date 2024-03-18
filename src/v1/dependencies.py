from typing import Annotated

from fastapi import Depends

from common.unitofwork import AbstractUnitOfWork, SqlAlchemyUnitOfWork

UOWDep = Annotated[AbstractUnitOfWork, Depends(SqlAlchemyUnitOfWork)]
