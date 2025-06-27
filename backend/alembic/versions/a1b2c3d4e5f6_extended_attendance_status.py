"""extended attendance status

Revision ID: a1b2c3d4e5f6
Revises: 810c85aedd55
Create Date: 2025-07-01 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '810c85aedd55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = sa.Enum(
        'present',
        'absent',
        'sick',
        'late',
        'excused',
        name='attendance_status_enum',
    )
    status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('attendance', sa.Column('status', status_enum, nullable=True))
    op.add_column('attendance', sa.Column('minutes_late', sa.SmallInteger(), nullable=True))
    op.add_column('attendance', sa.Column('comment', sa.Text(), nullable=True))
    op.execute("UPDATE attendance SET status='present' WHERE is_present = TRUE")
    op.execute("UPDATE attendance SET status='absent' WHERE is_present = FALSE")
    op.alter_column('attendance', 'status', nullable=False)
    op.drop_column('attendance', 'is_present')


def downgrade() -> None:
    op.add_column('attendance', sa.Column('is_present', sa.Boolean(), nullable=True))
    op.execute("UPDATE attendance SET is_present = (status='present')")
    op.alter_column('attendance', 'is_present', nullable=False)
    op.drop_column('attendance', 'comment')
    op.drop_column('attendance', 'minutes_late')
    op.drop_column('attendance', 'status')
    op.execute('DROP TYPE IF EXISTS attendance_status_enum')

