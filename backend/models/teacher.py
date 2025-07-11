# backend/models/teacher.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .class_ import ClassTeacherRoleAssociation
from core.db import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=False)
    contact_info = Column(String(100), nullable=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, unique=True)
    is_active = Column(Boolean, nullable=False, server_default='true')

    # Отношения
    subjects = relationship('Subject', secondary='teacher_subjects', back_populates='teachers')
    grades = relationship('Grade', back_populates='teacher', cascade='all, delete-orphan')
    schedules = relationship('Schedule', back_populates='teacher', cascade='all, delete-orphan')
    school = relationship('School', back_populates='teachers')
    user = relationship('User', back_populates='teacher')
    teacher_subjects = relationship(
        'TeacherSubject',
        back_populates='teacher',
        cascade='all, delete-orphan'
    )
    classes = relationship('Class', secondary='class_teachers', back_populates='teachers')
    class_teachers = relationship('ClassTeacher', back_populates='teacher', cascade='all, delete-orphan')
    homeroom_classes = relationship(
        'Class',
        secondary='class_teacher_roles',
        primaryjoin="and_(Teacher.id==ClassTeacherRoleAssociation.teacher_id, ClassTeacherRoleAssociation.role=='homeroom')",
        secondaryjoin="Class.id==ClassTeacherRoleAssociation.class_id",
        viewonly=True,
    )
