"""add subject aliases

Revision ID: da2c6a68a1cc
Revises: e4b7c1dca9e6
Create Date: 2025-06-27 08:02:06.682786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da2c6a68a1cc'
down_revision: Union[str, None] = 'e4b7c1dca9e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'subject_aliases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('alias', sa.Text(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('alias'),
    )


def downgrade() -> None:
    op.drop_table('subject_aliases')
