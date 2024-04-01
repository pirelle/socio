from sqlalchemy import Boolean, ForeignKey, Integer, String, Enum, true
from sqlalchemy.orm import Mapped, mapped_column

from common.database import BaseWithId, CreatedUpdatedMixin
from posts.enums import ContentType
from posts.schemas import CommentSchema, ImageSchema, PostSchema
from users.models import User


class Post(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_post"
    schema_to_read = PostSchema

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    text: Mapped[str] = mapped_column(String(1000), nullable=True)
    allow_comments: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )


class Image(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_image"
    schema_to_read = ImageSchema

    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    image_path: Mapped[str] = mapped_column(String())
    order: Mapped[int] = mapped_column(Integer())


class Comment(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_comment"
    schema_to_read = CommentSchema

    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    text: Mapped[str] = mapped_column(String(500))


class Like(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "posts_like"

    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType))
    content_id: Mapped[int] = mapped_column(Integer())
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
