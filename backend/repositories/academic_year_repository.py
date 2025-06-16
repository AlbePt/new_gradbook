# backend/repositories/academic_year_repository.py
from sqlalchemy.orm import Session
from models.academic_year import AcademicYear
from schemas.academic_year import AcademicYearCreate

class AcademicYearRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, year_id: int) -> AcademicYear | None:
        return self.db.query(AcademicYear).filter(AcademicYear.id == year_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(AcademicYear).offset(skip).limit(limit).all()

    def create(self, year: AcademicYearCreate) -> AcademicYear:
        db_year = AcademicYear(**year.dict())
        self.db.add(db_year)
        self.db.commit()
        self.db.refresh(db_year)
        return db_year

    def update(self, year_id: int, updates: dict) -> AcademicYear:
        db_year = self.get(year_id)
        for key, value in updates.items():
            setattr(db_year, key, value)
        self.db.commit()
        self.db.refresh(db_year)
        return db_year

    def delete(self, year_id: int) -> None:
        db_year = self.get(year_id)
        if db_year:
            self.db.delete(db_year)
            self.db.commit()
