# backend/repositories/student_repository.py
from sqlalchemy.orm import Session
from models.student import Student
from schemas.student import StudentCreate, StudentRead

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, student_id: int) -> Student:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Student).offset(skip).limit(limit).all()

    def create(self, student: StudentCreate) -> Student:
        db_student = Student(**student.dict())
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def update(self, student_id: int, updates: dict) -> Student:
        db_student = self.get(student_id)
        for key, value in updates.items():
            setattr(db_student, key, value)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def delete(self, student_id: int) -> None:
        db_student = self.get(student_id)
        if db_student:
            self.db.delete(db_student)
            self.db.commit()