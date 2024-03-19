from pydantic import EmailStr

from common.schemas import CreatedUpdatedSchema
from posts.schemas import PostSchema
from users.enums import UserType


class UserSchemaAdd(CreatedUpdatedSchema):
    first_name: str
    last_name: str
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
