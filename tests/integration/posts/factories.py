import factory.fuzzy

from common.database import mssql_sync_session
from posts.models import Post, Comment, Like
from tests.integration.users.factories import UserFactory


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = mssql_sync_session

    user_id = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence")
    allow_comments = factory.fuzzy.FuzzyChoice([True, False])
    is_published = factory.fuzzy.FuzzyChoice([True, False])


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = mssql_sync_session

    user_id = factory.SubFactory(UserFactory)
    post_id = factory.SubFactory(PostFactory)
    text = factory.Faker("sentence")


class LikeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Like
        sqlalchemy_session = mssql_sync_session
