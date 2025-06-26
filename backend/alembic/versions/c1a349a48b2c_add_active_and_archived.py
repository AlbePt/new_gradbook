"""add active flag to teacher and archived flag to class

Revision ID: c1a349a48b2c
Revises: aeedbaddcafe
Create Date: 2025-07-30 12:00:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c1a349a48b2c'
down_revision: Union[str, None] = 'aeedbaddcafe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('teachers', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('classes', sa.Column('is_archived', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('classes', 'is_archived')
    op.drop_column('teachers', 'is_active')
