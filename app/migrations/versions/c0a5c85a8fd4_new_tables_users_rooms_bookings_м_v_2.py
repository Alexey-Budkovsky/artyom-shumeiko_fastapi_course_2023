"""New tables: Users, Rooms, Bookings. М V_2

Revision ID: c0a5c85a8fd4
Revises: 4660dfd601e1
Create Date: 2024-09-04 14:58:46.428501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0a5c85a8fd4'
down_revision: Union[str, None] = '4660dfd601e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookings', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bookings', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
