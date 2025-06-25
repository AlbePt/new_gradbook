"""add full_name column to schools

Revision ID: 1e8d45aee0f1
Revises: aeedbaddcafe
Create Date: 2025-08-31 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '1e8d45aee0f1'
# previous revision
down_revision: Union[str, None] = 'aeedbaddcafe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('schools', sa.Column('full_name', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('schools', 'full_name')

