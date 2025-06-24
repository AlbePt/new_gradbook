# backend/models/class_.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from core.db import Base

# Association table between classes and subjects
class_subjects = Table(
    'class_subjects',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id', ondelete='CASCADE'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)
)

# Association table between classes and teachers
class_teachers = Table(
    'class_teachers',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id', ondelete='CASCADE'), primary_key=True),
    Column('teacher_id', Integer, ForeignKey('teachers.id', ondelete='CASCADE'), primary_key=True)
)


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), unique=True, nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    school = relationship('School', back_populates='classes')
    students = relationship('Student', back_populates='school_class', cascade='all, delete-orphan')
    subjects = relationship('Subject', secondary=class_subjects, back_populates='classes')
    teachers = relationship('Teacher', secondary=class_teachers, back_populates='classes')
