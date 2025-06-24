"""into full_name

Revision ID: 8f7055f0ed79
Revises: 0c51b27e6020
Create Date: 2025-06-23 14:59:07.429226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f7055f0ed79'
down_revision: Union[str, None] = '0c51b27e6020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
