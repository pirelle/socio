from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.orm import Session

from utils.database import async_session_maker, get_session, get_async_session
from users.repositories import UserRepository
from posts.repositories import PostRepository, ImageRepository, CommentRepository


class AbstractUnitOfWork(ABC):
    users: UserRepository
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
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()  # type: AsyncSession
        self.users = UserRepository(self.session)
        self.posts = PostRepository(self.session)
        self.images = ImageRepository(self.session)
        self.comments = CommentRepository(self.session)

    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
