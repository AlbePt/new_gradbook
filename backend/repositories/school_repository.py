# backend/repositories/school_repository.py
from sqlalchemy.orm import Session
from models.school import School
from schemas.school import SchoolCreate

class SchoolRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, school_id: int) -> School | None:
        return self.db.query(School).filter(School.id == school_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(School).offset(skip).limit(limit).all()

    def create(self, school: SchoolCreate) -> School:
        db_school = School(**school.dict())
        self.db.add(db_school)
        self.db.commit()
        self.db.refresh(db_school)
        return db_school

    def update(self, school_id: int, updates: dict) -> School:
        db_school = self.get(school_id)
        for key, value in updates.items():
            setattr(db_school, key, value)
        self.db.commit()
        self.db.refresh(db_school)
        return db_school

    def delete(self, school_id: int) -> None:
        db_school = self.get(school_id)
        if db_school:
            self.db.delete(db_school)
            self.db.commit()
