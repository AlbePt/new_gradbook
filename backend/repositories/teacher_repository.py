# backend/repositories/teacher_repository.py
from sqlalchemy.orm import Session
from models.teacher import Teacher
from schemas.teacher import TeacherCreate

class TeacherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, teacher_id: int) -> Teacher:
        return self.db.query(Teacher).filter(Teacher.id == teacher_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Teacher).offset(skip).limit(limit).all()

    def create(self, teacher: TeacherCreate) -> Teacher:
        db_teacher = Teacher(**teacher.dict())
        self.db.add(db_teacher)
        self.db.commit()
        self.db.refresh(db_teacher)
        return db_teacher

    def update(self, teacher_id: int, updates: dict) -> Teacher:
        db_teacher = self.get(teacher_id)
        for key, value in updates.items():
            setattr(db_teacher, key, value)
        self.db.commit()
        self.db.refresh(db_teacher)
        return db_teacher

    def delete(self, teacher_id: int) -> None:
        db_teacher = self.get(teacher_id)
        if db_teacher:
            self.db.delete(db_teacher)
            self.db.commit()
