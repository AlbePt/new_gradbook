"""split class teacher roles into separate table

Revision ID: abc123456789
Revises: 1e8d45aee0f1
Create Date: 2025-09-01 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'abc123456789'
down_revision: Union[str, None] = '1e8d45aee0f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'class_teacher_roles',
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('academic_year_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ['class_id', 'teacher_id', 'academic_year_id'],
            ['class_teachers.class_id',
             'class_teachers.teacher_id',
             'class_teachers.academic_year_id'],
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('class_id', 'teacher_id',
                                'academic_year_id', 'role'),
    )

    # ⚠️  CНАЧАЛА убрать индекс со старой таблицы
    op.drop_index('uq_one_homeroom_per_class',
                  table_name='class_teachers')

    # затем создать новый на новой таблице
    op.create_index(
        'uq_one_homeroom_per_class',
        'class_teacher_roles',
        ['class_id', 'academic_year_id'],
        unique=True,
        postgresql_where=sa.text("role = 'homeroom'"),
    )

    op.execute("""
        INSERT INTO class_teacher_roles(class_id, teacher_id,
                                        academic_year_id, role)
        SELECT class_id, teacher_id, academic_year_id, role
        FROM class_teachers
    """)

    op.drop_constraint('chk_class_teacher_role',
                       'class_teachers', type_='check')
    op.drop_column('class_teachers', 'role')


def downgrade() -> None:
    op.add_column(
        'class_teachers',
        sa.Column('role', sa.String(length=20), nullable=False, server_default='regular')
    )
    op.create_check_constraint(
        'chk_class_teacher_role',
        'class_teachers',
        "role IN ('regular','homeroom','assistant')",
    )
    op.create_index(
        'uq_one_homeroom_per_class',
        'class_teachers',
        ['class_id', 'academic_year_id'],
        unique=True,
        postgresql_where=sa.text("role = 'homeroom'"),
    )

    op.execute(
        "INSERT INTO class_teachers(class_id, teacher_id, academic_year_id, role) "
        "SELECT class_id, teacher_id, academic_year_id, role FROM class_teacher_roles"
    )

    op.drop_index('uq_one_homeroom_per_class', table_name='class_teacher_roles')
    op.drop_table('class_teacher_roles')
