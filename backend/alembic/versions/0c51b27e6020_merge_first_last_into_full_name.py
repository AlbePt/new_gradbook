"""merge first+last into full_name

Revision ID: 0c51b27e6020
Revises: e7b4bfe693a4
Create Date: 2025-06-23 12:55:16.085796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c51b27e6020'
down_revision: Union[str, None] = 'e7b4bfe693a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
