from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from users.enums import UserType
from users.schemas import UserSchema
from utils.database import BaseWithId, CreatedUpdatedMixin


class User(CreatedUpdatedMixin, BaseWithId):
    __tablename__ = "users_user"
    schema_to_read = UserSchema

    first_name: Mapped[str] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(32), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))
