# backend/models/class_.py
import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Enum,
    UniqueConstraint,
    ForeignKeyConstraint,
    Index,
    text,
    Boolean,
)
from sqlalchemy.orm import relationship

from core.db import Base

# Association table between classes and subjects
class_subjects = Table(
    'class_subjects',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id', ondelete='CASCADE'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)
)

class ClassTeacherRole(str, enum.Enum):
    regular = "regular"
    homeroom = "homeroom"
    assistant = "assistant"


class ClassTeacher(Base):
    __tablename__ = 'class_teachers'

    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), primary_key=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id', ondelete='CASCADE'), primary_key=True)

    school_class = relationship('Class', back_populates='class_teachers')
    teacher = relationship('Teacher', back_populates='class_teachers')
    academic_year = relationship('AcademicYear', back_populates='class_teachers')
    roles = relationship(
        'ClassTeacherRoleAssociation',
        back_populates='class_teacher',
        cascade='all, delete-orphan',
    )


class ClassTeacherRoleAssociation(Base):
    __tablename__ = 'class_teacher_roles'

    class_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, primary_key=True)
    academic_year_id = Column(Integer, primary_key=True)
    role = Column(Enum(ClassTeacherRole), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['class_id', 'teacher_id', 'academic_year_id'],
            ['class_teachers.class_id', 'class_teachers.teacher_id', 'class_teachers.academic_year_id'],
            ondelete='CASCADE',
        ),
    )

    class_teacher = relationship('ClassTeacher', back_populates='roles')

# Unique index ensuring only one homeroom teacher per class and year
Index(
    'uq_one_homeroom_per_class',
    ClassTeacherRoleAssociation.class_id,
    ClassTeacherRoleAssociation.academic_year_id,
    unique=True,
    postgresql_where=text("role = 'homeroom'"),
)


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id', ondelete='CASCADE'), nullable=False)
    is_archived = Column(Boolean, nullable=False, server_default='false')

    __table_args__ = (
        UniqueConstraint('name', 'school_id', 'academic_year_id'),
    )

    # Relationships
    school = relationship('School', back_populates='classes')
    academic_year = relationship('AcademicYear', back_populates='classes')
    students = relationship('Student', back_populates='school_class', cascade='all, delete-orphan')
    subjects = relationship('Subject', secondary=class_subjects, back_populates='classes')
    teachers = relationship('Teacher', secondary='class_teachers', back_populates='classes')
    class_teachers = relationship('ClassTeacher', back_populates='school_class', cascade='all, delete-orphan')
    homeroom_teachers = relationship(
        'Teacher',
        secondary='class_teacher_roles',
        primaryjoin="and_(Class.id==ClassTeacherRoleAssociation.class_id, ClassTeacherRoleAssociation.role=='homeroom')",
        secondaryjoin="Teacher.id==ClassTeacherRoleAssociation.teacher_id",
        viewonly=True,
    )
