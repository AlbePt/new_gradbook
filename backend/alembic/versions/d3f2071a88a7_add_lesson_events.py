"""add lesson events

Revision ID: d3f2071a88a7
Revises: a1b2c3d4e5f6
Create Date: 2025-06-27 07:20:02.461162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f2071a88a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lesson_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("lesson_date", sa.Date(), nullable=False),
        sa.Column("lesson_index", sa.SmallInteger(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
    )
    op.add_column(
        "grades",
        sa.Column("lesson_event_id", sa.BigInteger(), nullable=False),
    )
    op.create_foreign_key(
        None, "grades", "lesson_events", ["lesson_event_id"], ["id"], ondelete="CASCADE"
    )
    op.alter_column("grades", "lesson_event_id", nullable=False)
    op.add_column(
        "attendance",
        sa.Column("lesson_event_id", sa.BigInteger(), nullable=False),
    )
    op.create_foreign_key(
        None, "attendance", "lesson_events", ["lesson_event_id"], ["id"], ondelete="CASCADE"
    )
    op.alter_column("attendance", "lesson_event_id", nullable=False)


def downgrade() -> None:
    op.drop_constraint(None, "attendance", type_="foreignkey")
    op.drop_column("attendance", "lesson_event_id")
    op.drop_constraint(None, "grades", type_="foreignkey")
    op.drop_column("grades", "lesson_event_id")
    op.drop_table("lesson_events")
