from jose import jwt

from users.schemas import UserSchema, UserSchemaAdd
from config import SECRET_KEY


class UserService:
    def __init__(
        self,
        uow,
        encrypt_password_strat,
        verify_password_strat,
    ):
        self.uow = uow
        self._encrypt_password_strat = encrypt_password_strat
        self._verify_password_strat = verify_password_strat

    def encrypt_password(self, password):
        return self._encrypt_password_strat(password)

    def verify_password(self, password, hashed):
        return self._verify_password_strat(password, hashed)

    async def add_user(self, user: UserSchemaAdd) -> int:
        async with self.uow:
            user_id = await self.uow.users.add(
                {**user.model_dump(), "password": self.encrypt_password(user.password)}
            )
            await self.uow.commit()
            return user_id

    async def get_users(self) -> list[UserSchema]:
        async with self.uow:
            users = await self.uow.users.get_all()
            return users

    async def get_user(self, email: str) -> UserSchema:
        async with self.uow:
            user = await self.uow.users.get(email=email)
        return user

    async def authenticate_user(
        self, username: str, password: str
    ) -> UserSchema | None:
        async with self.uow:
            user = await self.get_user(username)
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        data = jwt.decode(token, SECRET_KEY)
        return data
