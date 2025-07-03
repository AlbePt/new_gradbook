"""add unique constraint for attendance student/date

Revision ID: ad004e2829b1
Revises: 51f043c35f8f
Create Date: 2025-07-10 00:00:00
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'ad004e2829b1'
down_revision: Union[str, Sequence[str], None] = '51f043c35f8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uix_student_date', 'attendance', ['student_id', 'date'])


def downgrade() -> None:
    op.drop_constraint('uix_student_date', 'attendance', type_='unique')
