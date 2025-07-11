"""add full_name to users and teacher.user_id

Revision ID: a1b2c3d4e5f7
Revises: f9f3a08e243c
Create Date: 2025-09-01 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f7'
down_revision: Union[str, None] = 'f9f3a08e243c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('full_name', sa.String(length=50), nullable=True))
    op.add_column('teachers', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_unique_constraint('uq_teacher_user', 'teachers', ['user_id'])
    op.create_foreign_key(None, 'teachers', 'users', ['user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint(None, 'teachers', type_='foreignkey')
    op.drop_constraint('uq_teacher_user', 'teachers', type_='unique')
    op.drop_column('teachers', 'user_id')
    op.drop_column('users', 'full_name')
