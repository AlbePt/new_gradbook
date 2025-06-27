from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.db import Base


class SubjectAlias(Base):
    __tablename__ = "subject_aliases"

    id = Column(Integer, primary_key=True)
    alias = Column(Text, unique=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    subject = relationship("Subject", back_populates="aliases")

