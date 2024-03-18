import factory.fuzzy

from tests.conftest import session
from users.enums import UserType
from users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = True
    user_type = factory.fuzzy.FuzzyChoice(UserType)
