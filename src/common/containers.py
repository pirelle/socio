from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Resource

from common.database import get_async_session_maker
from common.unitofwork import AbstractUnitOfWork, SqlAlchemyUnitOfWork


class Container(DeclarativeContainer):
    async_session_maker = Resource(get_async_session_maker)
    uow: AbstractUnitOfWork = Factory(
        SqlAlchemyUnitOfWork,
        session_maker=async_session_maker,
    )
