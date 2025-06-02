# backend/models/parent.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    messenger_id = Column(String(50), nullable=True)

    children = relationship('Student', back_populates='parent')
