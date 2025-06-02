# backend/repositories/attendance_repository.py
from sqlalchemy.orm import Session
from models.attendance import Attendance
from schemas.attendance import AttendanceCreate

class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, attendance_id: int) -> Attendance:
        return self.db.query(Attendance).filter(Attendance.id == attendance_id).first()

    def get_by_student_date(self, student_id: int, date):
        return self.db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date == date
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Attendance).offset(skip).limit(limit).all()

    def create(self, attendance: AttendanceCreate) -> Attendance:
        db_att = Attendance(**attendance.dict())
        self.db.add(db_att)
        self.db.commit()
        self.db.refresh(db_att)
        return db_att

    def update(self, attendance_id: int, updates: dict) -> Attendance:
        db_att = self.get(attendance_id)
        for key, value in updates.items():
            setattr(db_att, key, value)
        self.db.commit()
        self.db.refresh(db_att)
        return db_att

    def delete(self, attendance_id: int) -> None:
        db_att = self.get(attendance_id)
        if db_att:
            self.db.delete(db_att)
            self.db.commit()

