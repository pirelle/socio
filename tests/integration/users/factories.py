import factory.fuzzy

from users.enums import UserType
from users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = True
    user_type = factory.fuzzy.FuzzyChoice(UserType)
