"""post title to text

Revision ID: ef5587c805a3
Revises: e11c355791d3
Create Date: 2024-03-13 10:49:52.331731

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ef5587c805a3"
down_revision: Union[str, None] = "e11c355791d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("posts_post", "title", new_column_name="text")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("posts_post", "text", new_column_name="title")
    # ### end Alembic commands ###
