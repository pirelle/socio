from users.models import Follower, User
from common.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User


class FollowerRepository(SQLAlchemyRepository):
    model = Follower
