"""add term and grade kind enums

Revision ID: 1cf1420fbe73
Revises: f7cc120ae15a
Create Date: 2025-08-01 00:00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1cf1420fbe73"
down_revision: Union[str, None] = "f7cc120ae15a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    term_type_enum = sa.Enum(
        "trimester", "quarter", "semester", "year", name="term_type_enum"
    )
    grade_kind_enum = sa.Enum(
        "regular",
        "avg",
        "weighted_avg",
        "period_final",
        "year_final",
        "exam",
        "state_exam",
        name="grade_kind_enum",
    )
    term_type_enum.create(op.get_bind(), checkfirst=True)
    grade_kind_enum.create(op.get_bind(), checkfirst=True)
    op.add_column("grades", sa.Column("term_type", term_type_enum, nullable=False))
    op.add_column("grades", sa.Column("term_index", sa.SmallInteger(), nullable=False))
    op.add_column("grades", sa.Column("grade_kind", grade_kind_enum, nullable=False))
    op.add_column("grades", sa.Column("lesson_event_id", sa.Integer(), nullable=True))
    op.alter_column("grades", "value", type_=sa.Numeric(4, 2))
    op.create_index(
        "uq_grade_unique",
        "grades",
        [
            "student_id",
            "subject_id",
            "term_type",
            "term_index",
            "grade_kind",
            "lesson_event_id",
        ],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_grade_unique", table_name="grades")
    op.alter_column("grades", "value", type_=sa.Integer())
    op.drop_column("grades", "lesson_event_id")
    op.drop_column("grades", "grade_kind")
    op.drop_column("grades", "term_index")
    op.drop_column("grades", "term_type")
    op.execute("DROP TYPE IF EXISTS grade_kind_enum")
    op.execute("DROP TYPE IF EXISTS term_type_enum")
