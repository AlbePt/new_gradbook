"""add lesson events

Revision ID: d3f2071a88a7
Revises: a1b2c3d4e5f6
Create Date: 2025-06-27 07:20:02.461162
"""
from typing import Union, Sequence
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'd3f2071a88a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) создаём таблицу lesson_events
    op.create_table(
        "lesson_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("lesson_date", sa.Date(), nullable=False),
        sa.Column("lesson_index", sa.SmallInteger(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
    )

    bind = op.get_bind()
    insp = inspect(bind)

    # 2) grades ➞ lesson_event_id
    if "grades" in insp.get_table_names():
        cols = [c["name"] for c in insp.get_columns("grades")]
        if "lesson_event_id" not in cols:
            op.add_column(
                "grades",
                sa.Column("lesson_event_id", sa.BigInteger(), nullable=False),
            )
            op.create_foreign_key(
                None,
                "grades",
                "lesson_events",
                ["lesson_event_id"],
                ["id"],
                ondelete="CASCADE",
            )
            op.alter_column("grades", "lesson_event_id", nullable=False)

    # 3) attendance ➞ lesson_event_id
    if "attendance" in insp.get_table_names():
        cols = [c["name"] for c in insp.get_columns("attendance")]
        if "lesson_event_id" not in cols:
            op.add_column(
                "attendance",
                sa.Column("lesson_event_id", sa.BigInteger(), nullable=False),
            )
            op.create_foreign_key(
                None,
                "attendance",
                "lesson_events",
                ["lesson_event_id"],
                ["id"],
                ondelete="CASCADE",
            )
            op.alter_column("attendance", "lesson_event_id", nullable=False)


def downgrade() -> None:
    # при даунграде просто удаляем то, что создали
    op.drop_constraint(None, "attendance", type_="foreignkey")
    op.drop_column("attendance", "lesson_event_id")

    op.drop_constraint(None, "grades", type_="foreignkey")
    op.drop_column("grades", "lesson_event_id")

    op.drop_table("lesson_events")
