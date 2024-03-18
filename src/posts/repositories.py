from common.repository import SQLAlchemyRepository
from posts.models import Comment, Image, Post


class PostRepository(SQLAlchemyRepository):
    model = Post


class ImageRepository(SQLAlchemyRepository):
    model = Image


class CommentRepository(SQLAlchemyRepository):
    model = Comment
