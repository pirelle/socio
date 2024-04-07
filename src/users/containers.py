from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Resource, Factory

from users.services import UserService
from common.containers import Container as CommonContainer
from users.utils import encrypt_password_strat, verify_password_strat


class Container(DeclarativeContainer):
    uow = Resource(CommonContainer.uow)

    user_service = Factory(
        UserService,
        uow=uow,
        encrypt_password_strat=encrypt_password_strat,
        verify_password_strat=verify_password_strat,
    )
