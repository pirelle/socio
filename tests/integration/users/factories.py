import factory.fuzzy

from users.enums import UserType
from users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    def __init__(self, *args, session=None, **kwargs):
        self._meta.sqlalchemy_session = session
        super().__init__(self, *args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, session=None, **kwargs):
        cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    class Meta:
        model = User
        # sqlalchemy_session = session
        # sqlalchemy_session_persistence = SESSION_PERSISTENCE_COMMIT

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = True
    user_type = factory.fuzzy.FuzzyChoice(UserType)
