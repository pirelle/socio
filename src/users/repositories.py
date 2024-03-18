from users.models import User, Follower
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User


class FollowerRepository(SQLAlchemyRepository):
    model = Follower
