from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from common.database import BaseWithId, CreatedUpdatedMixin
from users.enums import UserType
from users.schemas import FollowerSchema, UserSchema


class User(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "users_user"
    schema_to_read = UserSchema

    first_name: Mapped[str] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))


class Follower(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "users_follower"
    schema_to_read = FollowerSchema

    follower_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    following_id: Mapped[int] = mapped_column(ForeignKey(User.id))
