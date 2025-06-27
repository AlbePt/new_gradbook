"""add exams table

Revision ID: e4b7c1dca9e6
Revises: d3f2071a88a7
Create Date: 2025-07-09 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e4b7c1dca9e6'
down_revision: Union[str, None] = 'd3f2071a88a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exams',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('student_id', sa.BigInteger(), nullable=False),
        sa.Column('subject_id', sa.BigInteger(), nullable=False),
        sa.Column('exam_kind', sa.String(length=50), nullable=False),
        sa.Column('exam_date', sa.Date(), nullable=False),
        sa.Column('value', sa.SmallInteger(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('exams')
