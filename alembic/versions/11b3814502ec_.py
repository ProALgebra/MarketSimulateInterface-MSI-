"""empty message

Revision ID: 11b3814502ec
Revises: 217406ac7bdc
Create Date: 2023-11-14 23:26:23.107254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11b3814502ec'
down_revision: Union[str, None] = '217406ac7bdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.UUID(), nullable=False),
    sa.Column('date_from', sa.DateTime(), nullable=False),
    sa.Column('date_to', sa.DateTime(), nullable=False),
    sa.Column('commission', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('task_id', name=op.f('pk_task'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###
