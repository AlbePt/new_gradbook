"""add role to class teacher

Revision ID: f7cc120ae15a
Revises: 597cb480e371
Create Date: 2025-06-24 06:03:51.879332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7cc120ae15a'
down_revision: Union[str, None] = '597cb480e371'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('class_teachers', sa.Column('role', sa.Enum('homeroom', 'assistant', name='classteacherrole'), nullable=False, server_default='assistant'))
    op.alter_column('class_teachers', 'role', server_default=None)


def downgrade() -> None:
    op.drop_column('class_teachers', 'role')
    op.execute('DROP TYPE IF EXISTS classteacherrole')
