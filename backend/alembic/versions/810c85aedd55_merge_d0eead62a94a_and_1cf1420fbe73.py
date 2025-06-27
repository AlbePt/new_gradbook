"""Merge d0eead62a94a and 1cf1420fbe73

Revision ID: 810c85aedd55
Revises: d0eead62a94a, 1cf1420fbe73
Create Date: 2025-06-27 11:50:53.084148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '810c85aedd55'
down_revision: Union[str, None] = ('d0eead62a94a', '1cf1420fbe73')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
