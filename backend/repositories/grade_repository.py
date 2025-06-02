# backend/repositories/grade_repository.py
from sqlalchemy.orm import Session
from models.grade import Grade
from schemas.grade import GradeCreate

class GradeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, grade_id: int) -> Grade:
        return self.db.query(Grade).filter(Grade.id == grade_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Grade).offset(skip).limit(limit).all()

    def create(self, grade: GradeCreate) -> Grade:
        db_grade = Grade(**grade.dict())
        self.db.add(db_grade)
        self.db.commit()
        self.db.refresh(db_grade)
        return db_grade

    def update(self, grade_id: int, updates: dict) -> Grade:
        db_grade = self.get(grade_id)
        for key, value in updates.items():
            setattr(db_grade, key, value)
        self.db.commit()
        self.db.refresh(db_grade)
        return db_grade

    def delete(self, grade_id: int) -> None:
        db_grade = self.get(grade_id)
        if db_grade:
            self.db.delete(db_grade)
            self.db.commit()

