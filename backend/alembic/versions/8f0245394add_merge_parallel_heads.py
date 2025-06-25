"""merge parallel heads

Revision ID: 8f0245394add
Revises: 3f9608b15ced, abc123456789
Create Date: 2025-06-25 19:35:43.673664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f0245394add'
down_revision: Union[str, None] = ('3f9608b15ced', 'abc123456789')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
