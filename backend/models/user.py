import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class RoleEnum(str, enum.Enum):
    superuser = "superuser"
    administrator = "administrator"
    teacher = "teacher"
    student = "student"
    parent = "parent"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    full_name = Column(String(50), nullable=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=True)

    school = relationship('School', back_populates='users')
    teacher = relationship('Teacher', back_populates='user', uselist=False)

