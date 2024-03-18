from abc import ABC, abstractmethod

from common.database import async_session_maker
from common.repository import AbstractRepository
from posts.repositories import CommentRepository, ImageRepository, PostRepository
from users.repositories import UserRepository


class AbstractUnitOfWork(ABC):
    users: AbstractRepository
    posts: PostRepository
    images: ImageRepository
    comments: CommentRepository

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_maker=async_session_maker):
        self.session_factory = session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.posts = PostRepository(self.session)
        self.images = ImageRepository(self.session)
        self.comments = CommentRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
