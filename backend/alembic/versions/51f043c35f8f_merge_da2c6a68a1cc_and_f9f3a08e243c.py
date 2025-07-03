"""Merge da2c6a68a1cc and f9f3a08e243c

Revision ID: 51f043c35f8f
Revises: da2c6a68a1cc, f9f3a08e243c
Create Date: 2025-07-03 17:38:01.653193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51f043c35f8f'
down_revision: Union[str, None] = ('da2c6a68a1cc', 'f9f3a08e243c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
