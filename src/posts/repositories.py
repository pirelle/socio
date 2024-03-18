from posts.models import Comment, Image, Post
from common.repository import SQLAlchemyRepository


class PostRepository(SQLAlchemyRepository):
    model = Post


class ImageRepository(SQLAlchemyRepository):
    model = Image


class CommentRepository(SQLAlchemyRepository):
    model = Comment
