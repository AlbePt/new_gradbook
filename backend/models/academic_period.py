# backend/models/academic_period.py
from sqlalchemy import Column, Integer, Date, Enum, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from core.db import Base
from models.grade import TermTypeEnum

class AcademicPeriod(Base):
    __tablename__ = "academic_periods"

    id = Column(Integer, primary_key=True, index=True)
    academic_year_id = Column(
        Integer, ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False
    )
    term_type = Column(Enum(TermTypeEnum), nullable=False)
    term_index = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    academic_year = relationship("AcademicYear", back_populates="periods")
