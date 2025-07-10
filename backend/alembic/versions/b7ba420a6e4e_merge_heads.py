"""merge heads

Revision ID: b7ba420a6e4e
Revises: 24b0f0ffab91, 34497216cc86
Create Date: 2025-07-10 18:26:10.271644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7ba420a6e4e'
down_revision: Union[str, None] = ('24b0f0ffab91', '34497216cc86')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
