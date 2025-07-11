"""merge heads

Revision ID: b7460ebe2397
Revises: a1b2c3d4e5f7, b7ba420a6e4e
Create Date: 2025-07-11 11:24:20.557442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7460ebe2397'
down_revision: Union[str, None] = ('a1b2c3d4e5f7', 'b7ba420a6e4e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
