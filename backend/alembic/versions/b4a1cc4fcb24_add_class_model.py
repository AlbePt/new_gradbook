"""add class model

Revision ID: b4a1cc4fcb24
Revises: 8e8c61bf2b01
Create Date: 2025-07-12 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b4a1cc4fcb24'
down_revision = '8e8c61bf2b01'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'classes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=10), nullable=False),
        sa.Column('school_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_classes_id'), 'classes', ['id'], unique=False)

    op.add_column('students', sa.Column('class_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'students', 'classes', ['class_id'], ['id'], ondelete='CASCADE')

    op.create_table(
        'class_subjects',
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('class_id', 'subject_id')
    )

    op.create_table(
        'class_teachers',
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('class_id', 'teacher_id')
    )


def downgrade() -> None:
    op.drop_table('class_teachers')
    op.drop_table('class_subjects')
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.drop_column('students', 'class_id')
    op.drop_index(op.f('ix_classes_id'), table_name='classes')
    op.drop_table('classes')
