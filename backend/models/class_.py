# backend/models/class_.py
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
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
    role = Column(Enum(ClassTeacherRole), nullable=False)

    school_class = relationship('Class', back_populates='class_teachers')
    teacher = relationship('Teacher', back_populates='class_teachers')


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), unique=True, nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    school = relationship('School', back_populates='classes')
    students = relationship('Student', back_populates='school_class', cascade='all, delete-orphan')
    subjects = relationship('Subject', secondary=class_subjects, back_populates='classes')
    teachers = relationship('Teacher', secondary='class_teachers', back_populates='classes')
    class_teachers = relationship('ClassTeacher', back_populates='school_class', cascade='all, delete-orphan')
    homeroom_teachers = relationship(
        'Teacher',
        secondary='class_teachers',
        primaryjoin="and_(Class.id==ClassTeacher.class_id, ClassTeacher.role=='homeroom')",
        secondaryjoin="Teacher.id==ClassTeacher.teacher_id",
        viewonly=True,
    )
