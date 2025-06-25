"""add academic year relations

Revision ID: 3f9608b15ced
Revises: 1e8d45aee0f1
Create Date: 2025-06-25 08:29:25.186189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f9608b15ced'
down_revision: Union[str, None] = '1e8d45aee0f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('classes', sa.Column('academic_year_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'classes', 'academic_years', ['academic_year_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('classes_name_key', 'classes', type_='unique')
    op.create_unique_constraint('uq_class_name_school_year', 'classes', ['name', 'school_id', 'academic_year_id'])

    op.add_column('class_teachers', sa.Column('academic_year_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'class_teachers', 'academic_years', ['academic_year_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('class_teachers_pkey', 'class_teachers', type_='primary')
    op.create_primary_key('pk_class_teachers', 'class_teachers', ['class_id', 'teacher_id', 'academic_year_id'])
    op.drop_index('uq_one_homeroom_per_class', table_name='class_teachers')
    op.create_index('uq_one_homeroom_per_class', 'class_teachers', ['class_id', 'academic_year_id'], unique=True, postgresql_where=sa.text("role = 'homeroom'"))

    op.add_column('teacher_subjects', sa.Column('academic_year_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'teacher_subjects', 'academic_years', ['academic_year_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('teacher_subjects_pkey', 'teacher_subjects', type_='primary')
    op.create_primary_key('pk_teacher_subjects', 'teacher_subjects', ['teacher_id', 'subject_id', 'academic_year_id'])


def downgrade() -> None:
    op.drop_constraint('pk_teacher_subjects', 'teacher_subjects', type_='primary')
    op.create_primary_key('teacher_subjects_pkey', 'teacher_subjects', ['teacher_id', 'subject_id'])
    op.drop_constraint(None, 'teacher_subjects', type_='foreignkey')
    op.drop_column('teacher_subjects', 'academic_year_id')

    op.drop_index('uq_one_homeroom_per_class', table_name='class_teachers')
    op.drop_constraint('pk_class_teachers', 'class_teachers', type_='primary')
    op.create_primary_key('class_teachers_pkey', 'class_teachers', ['class_id', 'teacher_id'])
    op.drop_constraint(None, 'class_teachers', type_='foreignkey')
    op.drop_column('class_teachers', 'academic_year_id')

    op.drop_constraint('uq_class_name_school_year', 'classes', type_='unique')
    op.create_unique_constraint('classes_name_key', 'classes', ['name'])
    op.drop_constraint(None, 'classes', type_='foreignkey')
    op.drop_column('classes', 'academic_year_id')
