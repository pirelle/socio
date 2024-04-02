from sqlalchemy import select

from jose import jwt
from passlib.context import CryptContext

from users.models import User
from users.schemas import UserSchema, UserSchemaAdd
from config import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, uow):
        self.uow = uow

    async def add_user(self, user: UserSchemaAdd) -> int:
        user_dict = user.model_dump()
        async with self.uow:
            user_id = await self.uow.users.add(user_dict)
            await self.uow.commit()
            return user_id

    async def get_users(self) -> list[UserSchema]:
        async with self.uow:
            users = await self.uow.users.get_all()
            return users

    async def authenticate_user(
        self, username: str, password: str
    ) -> UserSchema | None:
        async with self.uow:
            user = await self.uow.users.get(email=username)
        if not user:
            return None
        if not pwd_context.verify(password, user.password):
            return None
        return user


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


class SyncUserService:
    def __init__(self, session):
        self.session = session

    def get_users(self) -> list[UserSchema]:
        stmt = select(User)
        res = self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
