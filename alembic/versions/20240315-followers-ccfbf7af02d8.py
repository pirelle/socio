"""followers

Revision ID: ccfbf7af02d8
Revises: ef5587c805a3
Create Date: 2024-03-15 21:39:43.643751

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ccfbf7af02d8"
down_revision: Union[str, None] = "ef5587c805a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users_follower",
        sa.Column("follower", sa.Integer(), nullable=False),
        sa.Column("following", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["follower"],
            ["users_user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["following"],
            ["users_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_follower")
    # ### end Alembic commands ###