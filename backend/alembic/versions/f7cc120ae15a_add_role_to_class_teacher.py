"""add role to class teacher

Revision ID: f7cc120ae15a
Revises: 597cb480e371
Create Date: 2025-06-24 06:03:51.879332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7cc120ae15a'
down_revision: Union[str, None] = '597cb480e371'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "class_teachers",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default="regular"
        )
    )
    op.create_check_constraint(
        "chk_class_teacher_role",
        "class_teachers",
        "role IN ('regular','homeroom','assistant')"
    )
    op.create_index(
        "uq_one_homeroom_per_class",
        "class_teachers",
        ["class_id"],
        unique=True,
        postgresql_where=sa.text("role = 'homeroom'")
    )

def downgrade() -> None:
    op.drop_index("uq_one_homeroom_per_class", table_name="class_teachers")
    op.drop_constraint("chk_class_teacher_role", "class_teachers", type_="check")
    op.drop_column("class_teachers", "role")