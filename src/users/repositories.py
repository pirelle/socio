from common.repository import SQLAlchemyRepository
from users.models import Follower, User


class UserRepository(SQLAlchemyRepository):
    model = User


class FollowerRepository(SQLAlchemyRepository):
    model = Follower
