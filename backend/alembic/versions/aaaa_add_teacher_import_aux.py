"""ensure teacher import constraints

Revision ID: aeedbaddcafe
Revises: f7cc120ae15a
Create Date: 2025-07-30 00:00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "aeedbaddcafe"
down_revision: Union[str, None] = "f7cc120ae15a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DO $$BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='chk_class_teacher_role') THEN
            ALTER TABLE class_teachers ADD CONSTRAINT chk_class_teacher_role CHECK (role IN ('regular','homeroom','assistant'));
        END IF;
        END$$;
        """
    )
    op.execute(
        """
        DO $$BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname='uq_one_homeroom_per_class') THEN
            CREATE UNIQUE INDEX uq_one_homeroom_per_class ON class_teachers(class_id) WHERE role='homeroom';
        END IF;
        END$$;
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_one_homeroom_per_class")
    op.execute(
        "ALTER TABLE class_teachers DROP CONSTRAINT IF EXISTS chk_class_teacher_role"
    )
