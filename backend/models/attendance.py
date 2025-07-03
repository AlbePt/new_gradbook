# backend/models/attendance.py
import enum
from sqlalchemy import (
    Column,
    Integer,
    Date,
    Enum,
    ForeignKey,
    SmallInteger,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from core.db import Base


class AttendanceStatusEnum(str, enum.Enum):
    present = "present"
    absent = "absent"
    sick = "sick"
    late = "late"
    excused = "excused"


STATUS_CHAR_MAP = {
    "Н": AttendanceStatusEnum.absent,
    "Б": AttendanceStatusEnum.sick,
    "О": AttendanceStatusEnum.late,
    "У": AttendanceStatusEnum.excused,
}

class Attendance(Base):
    __tablename__ = 'attendance'

    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='uix_student_date'),
    )

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatusEnum), nullable=False)
    minutes_late = Column(SmallInteger)
    comment = Column(Text)
    lesson_event_id = Column(
        Integer,
        ForeignKey('lesson_events.id', ondelete='CASCADE'),
        nullable=False,
    )
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    student = relationship('Student', back_populates='attendance_records')
    academic_year = relationship('AcademicYear', back_populates='attendance_records')
    lesson_event = relationship('LessonEvent', back_populates='attendance_records')
