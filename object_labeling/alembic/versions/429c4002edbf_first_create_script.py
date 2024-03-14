"""first create script

Revision ID: 429c4002edbf
Revises: 
Create Date: 2024-03-04 10:03:03.550553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '429c4002edbf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'streaming_data', 
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('uri', sa.String(), nullable=False),
        sa.Column('device_name', sa.String()),
        sa.Column('create_time', sa.DateTime()),
    )

    op.create_table(
        'label_data', 
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('streaming_data_id', sa.Integer(), nullable=False),
        sa.Column('equipment_no', sa.String()),
        sa.Column('x1', sa.Integer()),
        sa.Column('y1', sa.Integer()),
        sa.Column('x2', sa.Integer()),
        sa.Column('y2', sa.Integer()),
        sa.Column('create_time', sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table('streaming_data')
    op.drop_table('label_data')
