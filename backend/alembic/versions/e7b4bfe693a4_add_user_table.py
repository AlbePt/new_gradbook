"""add user table

Revision ID: e7b4bfe693a4
Revises: aed5d35f4b67
Create Date: 2025-07-11 00:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e7b4bfe693a4'
down_revision = 'aed5d35f4b67'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('superuser','administrator','teacher','student','parent', name='roleenum'), nullable=False),
        sa.UniqueConstraint('username'),
        sa.Index('ix_users_id', 'id'),
        sa.Index('ix_users_username', 'username')
    )


def downgrade() -> None:
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS roleenum')

