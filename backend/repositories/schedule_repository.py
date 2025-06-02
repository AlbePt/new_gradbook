# backend/repositories/schedule_repository.py
from sqlalchemy.orm import Session
from models.schedule import Schedule
from schemas.schedule import ScheduleCreate

class ScheduleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, schedule_id: int) -> Schedule:
        return self.db.query(Schedule).filter(Schedule.id == schedule_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Schedule).offset(skip).limit(limit).all()

    def create(self, schedule: ScheduleCreate) -> Schedule:
        db_schedule = Schedule(**schedule.dict())
        self.db.add(db_schedule)
        self.db.commit()
        self.db.refresh(db_schedule)
        return db_schedule

    def update(self, schedule_id: int, updates: dict) -> Schedule:
        db_schedule = self.get(schedule_id)
        for key, value in updates.items():
            setattr(db_schedule, key, value)
        self.db.commit()
        self.db.refresh(db_schedule)
        return db_schedule

    def delete(self, schedule_id: int) -> None:
        db_schedule = self.get(schedule_id)
        if db_schedule:
            self.db.delete(db_schedule)
            self.db.commit()

