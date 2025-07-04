"""add academic periods table

Revision ID: b754354c5821
Revises: ad004e2829b1
Create Date: 2025-09-01 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b754354c5821'
down_revision: Union[str, None] = 'ad004e2829b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    term_type_enum = postgresql.ENUM(
        'trimester',
        'quarter',
        'semester',
        'year',
        name='term_type_enum',
        create_type=False,
    )
    op.create_table(
        'academic_periods',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('term_type', term_type_enum, nullable=False),
        sa.Column('term_index', sa.SmallInteger(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['academic_year_id'], ['academic_years.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_academic_periods_id'), 'academic_periods', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_academic_periods_id'), table_name='academic_periods')
    op.drop_table('academic_periods')
