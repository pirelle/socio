from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from posts.schemas import CommentSchema, ImageSchema, PostSchema
from users.models import User
from common.database import BaseWithId, CreatedUpdatedMixin


class Post(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_post"
    schema_to_read = PostSchema

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    text: Mapped[str] = mapped_column(String(1000), nullable=True)
    allow_comments: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)


class Image(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_image"
    schema_to_read = ImageSchema

    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    order: Mapped[int] = mapped_column(Integer())


class Comment(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_comment"
    schema_to_read = CommentSchema

    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    text: Mapped[str] = mapped_column(String(500))
