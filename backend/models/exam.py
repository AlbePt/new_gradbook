import enum
from sqlalchemy import Column, BigInteger, Integer, ForeignKey, SmallInteger, Date, Text, Enum
from sqlalchemy.orm import relationship
from core.db import Base


class ExamKindEnum(str, enum.Enum):
    exam = "exam"
    state_exam = "state_exam"


class Exam(Base):
    __tablename__ = "exams"

    id = Column(BigInteger, primary_key=True, index=True)
    student_id = Column(BigInteger, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(BigInteger, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    exam_kind = Column(Enum(ExamKindEnum), nullable=False)
    exam_date = Column(Date, nullable=False)
    value = Column(SmallInteger)
    comment = Column(Text)

    student = relationship("Student")
    subject = relationship("Subject")
