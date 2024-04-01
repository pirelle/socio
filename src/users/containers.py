from dependency_injector import containers
from dependency_injector.containers import WiringConfiguration, DeclarativeContainer
from dependency_injector.providers import Resource, Provider, Factory

from common.database import session_maker, async_session_maker
from common.unitofwork import SqlAlchemyUnitOfWork
from users.services import UserService, SyncUserService
from common.containers import Container as CommonContainer


class Container(CommonContainer):
    user_service: UserService = Factory(
        UserService,
        uow=CommonContainer.uow,
    )

    session_maker = Resource(session_maker)

    sync_user_service: SyncUserService = Factory(
        SyncUserService,
        session=session_maker,
    )
