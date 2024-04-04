from pydantic import EmailStr, BaseModel

from common.schemas import CreatedUpdatedSchema
from posts.schemas import PostSchema
from users.enums import UserType


class BaseUserSchema(BaseModel):
    first_name: str
    last_name: str


class UserSchemaAdd(CreatedUpdatedSchema, BaseUserSchema):
    email: EmailStr
    password: str
    is_active: bool
    user_type: UserType


class FollowerSchema(CreatedUpdatedSchema):
    follower_id: int
    following_id: int


class UserSchema(UserSchemaAdd):
    id: int
    posts: list[PostSchema] | None = None
    followers: list[int] | None = None


class PublicUserSchema(BaseUserSchema):
    id: int
