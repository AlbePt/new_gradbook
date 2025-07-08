"""merge heads

Revision ID: 34497216cc86
Revises: b754354c5821, bbb1addlesson
Create Date: 2025-07-08 15:58:42.548055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34497216cc86'
down_revision: Union[str, None] = ('b754354c5821', 'bbb1addlesson')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
