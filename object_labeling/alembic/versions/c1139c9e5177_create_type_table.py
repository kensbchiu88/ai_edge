"""create type table

Revision ID: c1139c9e5177
Revises: 429c4002edbf
Create Date: 2024-03-07 10:47:08.832179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1139c9e5177'
down_revision: Union[str, None] = '429c4002edbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'type_data', 
        sa.Column('key', sa.String(), primary_key=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('create_time', sa.DateTime()),
    )

    op.add_column('label_data', sa.Column('type', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_table('type_data')
    op.drop_column('label_data', 'type')
