"""add ids

Revision ID: 160714da3313
Revises: 2c0f5cb7f93c
Create Date: 2024-03-19 21:13:37.729695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '160714da3313'
down_revision: Union[str, None] = '2c0f5cb7f93c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts_like',
    sa.Column('content_type', sa.Enum('POST', 'COMMENT', name='contenttype'), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users_follower', sa.Column('follower_id', sa.Integer(), nullable=False))
    op.add_column('users_follower', sa.Column('following_id', sa.Integer(), nullable=False))
    op.drop_constraint('users_follower_follower_fkey', 'users_follower', type_='foreignkey')
    op.drop_constraint('users_follower_following_fkey', 'users_follower', type_='foreignkey')
    op.create_foreign_key(None, 'users_follower', 'users_user', ['following_id'], ['id'])
    op.create_foreign_key(None, 'users_follower', 'users_user', ['follower_id'], ['id'])
    op.drop_column('users_follower', 'following')
    op.drop_column('users_follower', 'follower')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_follower', sa.Column('follower', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('users_follower', sa.Column('following', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users_follower', type_='foreignkey')
    op.drop_constraint(None, 'users_follower', type_='foreignkey')
    op.create_foreign_key('users_follower_following_fkey', 'users_follower', 'users_user', ['following'], ['id'])
    op.create_foreign_key('users_follower_follower_fkey', 'users_follower', 'users_user', ['follower'], ['id'])
    op.drop_column('users_follower', 'following_id')
    op.drop_column('users_follower', 'follower_id')
    op.drop_table('posts_like')
    # ### end Alembic commands ###
