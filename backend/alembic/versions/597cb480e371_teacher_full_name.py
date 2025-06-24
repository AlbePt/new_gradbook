"""merge teacher first+last into full_name

Revision ID: 597cb480e371
Revises: b4a1cc4fcb24
Create Date: 2025-07-12 00:00:01
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '597cb480e371'
down_revision: Union[str, None] = 'b4a1cc4fcb24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('teachers', sa.Column('full_name', sa.String(length=50), nullable=False))
    op.drop_column('teachers', 'first_name')
    op.drop_column('teachers', 'last_name')


def downgrade() -> None:
    op.add_column('teachers', sa.Column('first_name', sa.String(length=50), nullable=False))
    op.add_column('teachers', sa.Column('last_name', sa.String(length=50), nullable=False))
    op.drop_column('teachers', 'full_name')
