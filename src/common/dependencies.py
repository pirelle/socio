from typing import Annotated

from fastapi import Depends


from users.services import UserService
from users.containers import Container as UserContainer


# def get_uow():
#     return SqlAlchemyUnitOfWork(session_maker=async_session_maker)


# UOWDep = Annotated[
#     AbstractUnitOfWork,
#     Depends(get_uow),
# ]


# def get_user_service(uow: UOWDep):
#     return UserService(uow=uow)


user_container = UserContainer()


async def get_user_service_from_container():
    user_service = await user_container.user_service()
    return user_service


UserServiceDep = Annotated[UserService, Depends(get_user_service_from_container)]
