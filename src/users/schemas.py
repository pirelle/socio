from pydantic import EmailStr

from users.enums import UserType
from common.schemas import CreatedUpdatedSchema


class UserSchemaAdd(CreatedUpdatedSchema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_active: bool
    user_type: UserType


class UserSchema(UserSchemaAdd):
    id: int


class FollowerSchema(CreatedUpdatedSchema):
    follower_id: int
    following_id: int
