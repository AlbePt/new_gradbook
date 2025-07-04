# backend/repositories/academic_period_repository.py
from sqlalchemy.orm import Session

from models.academic_period import AcademicPeriod
from schemas.academic_period import AcademicPeriodCreate


class AcademicPeriodRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, period_id: int) -> AcademicPeriod | None:
        return self.db.query(AcademicPeriod).filter(AcademicPeriod.id == period_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(AcademicPeriod).offset(skip).limit(limit).all()

    def create(self, period: AcademicPeriodCreate) -> AcademicPeriod:
        db_period = AcademicPeriod(**period.dict())
        self.db.add(db_period)
        self.db.commit()
        self.db.refresh(db_period)
        return db_period

    def update(self, period_id: int, updates: dict) -> AcademicPeriod:
        db_period = self.get(period_id)
        for key, value in updates.items():
            setattr(db_period, key, value)
        self.db.commit()
        self.db.refresh(db_period)
        return db_period

    def delete(self, period_id: int) -> None:
        db_period = self.get(period_id)
        if db_period:
            self.db.delete(db_period)
            self.db.commit()

