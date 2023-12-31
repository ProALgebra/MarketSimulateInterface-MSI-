"""

Revision ID: 017f0ee13993
Revises: 06fa5f95d58b
Create Date: 2023-11-15 17:11:42.067281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '017f0ee13993'
down_revision: Union[str, None] = '06fa5f95d58b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'language')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('language', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
