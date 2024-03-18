"""initial

Revision ID: e11c355791d3
Revises:
Create Date: 2024-03-13 09:28:08.299278

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e11c355791d3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=30), nullable=True),
        sa.Column("last_name", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "user_type",
            sa.Enum("MODERATOR", "REGULAR", name="usertype"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "posts_post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=1000), nullable=True),
        sa.Column("allow_comments", sa.Boolean(), nullable=False),
        sa.Column("is_blocked", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posts_comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts_post.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posts_image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts_post.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posts_image")
    op.drop_table("posts_comment")
    op.drop_table("posts_post")
    op.drop_table("users_user")
    sa.Enum(name="usertype").drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###