from abc import ABC, abstractmethod
from inspect import isasyncgen

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
    def __init__(self, session_maker):
        self.session_factory = session_maker

    async def __aenter__(self):
        self.session = (
            await anext(self.session_factory)
            if isasyncgen(self.session_factory)
            else self.session_factory()
        )
        self.users = UserRepository(self.session)
        self.posts = PostRepository(self.session)
        self.images = ImageRepository(self.session)
        self.comments = CommentRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()
        if isasyncgen(self.session_factory):
            await anext(self.session_factory)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
