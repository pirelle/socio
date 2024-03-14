from abc import ABC, abstractmethod

from posts.repositories import CommentRepository, ImageRepository, PostRepository
from users.repositories import UserRepository
from utils.database import async_session_maker


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
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
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
