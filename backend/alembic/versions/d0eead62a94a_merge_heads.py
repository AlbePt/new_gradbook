"""merge heads

Revision ID: d0eead62a94a
Revises: abc123456789, c1a349a48b2c
Create Date: 2025-06-26 12:52:49.552768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0eead62a94a'
down_revision: Union[str, None] = ('abc123456789', 'c1a349a48b2c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
