"""add unique constraint to lesson_events

Revision ID: bbb1addlesson
Revises: aeedbaddcafe
Create Date: 2025-07-08 00:00:00
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'bbb1addlesson'
down_revision: Union[str, None] = 'aeedbaddcafe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_lesson_event_unique',
        'lesson_events',
        ['subject_id', 'class_id', 'lesson_date', 'lesson_index']
    )


def downgrade() -> None:
    op.drop_constraint('uq_lesson_event_unique', 'lesson_events', type_='unique')
