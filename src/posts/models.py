from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from users.models import User
from utils.database import Base, CreatedUpdatedMixin


class Post(CreatedUpdatedMixin, Base):
    __tablename__ = "posts_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    text: Mapped[str] = mapped_column(String(1000), nullable=True)
    allow_comments: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)


class Image(CreatedUpdatedMixin, Base):
    __tablename__ = "posts_image"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    order: Mapped[int] = mapped_column(Integer())


class Comment(CreatedUpdatedMixin, Base):
    __tablename__ = "posts_comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    text: Mapped[str] = mapped_column(String(500))
