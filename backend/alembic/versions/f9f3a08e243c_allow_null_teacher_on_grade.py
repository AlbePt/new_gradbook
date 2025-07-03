"""allow null teacher on grade

Revision ID: f9f3a08e243c
Revises: f7cc120ae15a
Create Date: 2025-07-30 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f9f3a08e243c'
down_revision: Union[str, None] = 'f7cc120ae15a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column('grades', 'teacher_id', existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    op.alter_column('grades', 'teacher_id', existing_type=sa.Integer(), nullable=False)
