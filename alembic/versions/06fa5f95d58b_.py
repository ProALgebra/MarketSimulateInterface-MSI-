"""empty message

Revision ID: 06fa5f95d58b
Revises: 72e6fe75cbee
Create Date: 2023-11-15 13:37:37.498823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06fa5f95d58b'
down_revision: Union[str, None] = '72e6fe75cbee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('start_cash', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'start_cash')
    # ### end Alembic commands ###