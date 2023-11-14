"""empty message

Revision ID: 217406ac7bdc
Revises: 
Create Date: 2023-11-14 15:55:00.975539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '217406ac7bdc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('day', sa.DateTime(), nullable=False),
    sa.Column('ticket', sa.String(), nullable=False),
    sa.Column('price', sa.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ticket'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('commisions', sa.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('tg_id', name=op.f('uq_users_tg_id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('ticket')
    # ### end Alembic commands ###
