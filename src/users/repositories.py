from sqlalchemy import select, func

from common.repository import SQLAlchemyRepository
from posts.models import Comment, Post
from users.models import Follower, User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_with_followers(self, user_id: int):
        follower_user_cte = (
            select(
                User.id,
                User.first_name,
            )
            .cte()
        )

        followers_cte = (
            select(
                Follower.following_id,
                func.array_agg(
                    func.json_build_object(
                        "id", Follower.follower_id,
                        "name", follower_user_cte.c.first_name,
                    )
                ).label("followers")
            )
            .join(
                follower_user_cte,
                follower_user_cte.c.id == Follower.follower_id
            )
            .group_by(Follower.following_id)
            .cte()
        )

        comments_cte = (
            select(
                Comment.post_id,
                func.array_agg(
                    func.json_build_object(
                        "id", Comment.id,
                        "user_id", Comment.user_id,
                        "created_at", Comment.created_at,
                        "text", Comment.text,
                    )
                ).label("comments")
            )
            .group_by(Comment.post_id)
            .order_by(Comment.created_at)
            .cte()
        )

        posts_cte = (
            select(
                Post.user_id,
                func.array_agg(
                    func.json_build_object(
                        "id", Post.id,
                        "title", Post.text,
                        "created_at", Post.created_at,
                        "comments", comments_cte.c.comments,
                    )
                ).label("posts")
            )
            .outerjoin(
                comments_cte,
                Post.id == comments_cte.c.post_id,
            )
            .group_by(Post.user_id)
            .cte()
        )

        stmt = (
            select(
                User,
                followers_cte.c.followers,
                posts_cte.c.posts,
            )
            .outerjoin(followers_cte, User.id == followers_cte.c.following_id)
            .outerjoin(posts_cte, User.id == posts_cte.c.user_id)
            .where(User.id == 1)
        )
        result = (await self.session.execute(stmt))
        breakpoint()
        return result

class FollowerRepository(SQLAlchemyRepository):
    model = Follower
