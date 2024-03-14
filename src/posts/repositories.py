from posts.models import Post, Image, Comment
from utils.repository import SQLAlchemyRepository


class PostRepository(SQLAlchemyRepository):
    model = Post


class ImageRepository(SQLAlchemyRepository):
    model = Image


class CommentRepository(SQLAlchemyRepository):
    model = Comment
