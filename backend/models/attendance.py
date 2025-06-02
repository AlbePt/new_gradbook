# backend/models/attendance.py
from sqlalchemy import Column, Integer, Date, Boolean, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.db import Base

class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='uix_student_date'),
    )

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, nullable=False)
    reason = Column(String(255), nullable=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False)

    student = relationship('Student', back_populates='attendance_records')
    academic_year = relationship('AcademicYear', back_populates='attendance_records')