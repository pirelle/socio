from users.enums import UserType
from utils.schemas import CreatedUpdatedSchema


class UserSchemaAdd(CreatedUpdatedSchema):
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool
    user_type: UserType


class UserSchema(UserSchemaAdd):
    id: int
