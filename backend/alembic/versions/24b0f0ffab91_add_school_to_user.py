"""add school_id to users table

Revision ID: 24b0f0ffab91
Revises: f9f3a08e243c
Create Date: 2025-08-01 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '24b0f0ffab91'
down_revision: Union[str, None] = 'f9f3a08e243c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('school_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'schools', ['school_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'school_id')
