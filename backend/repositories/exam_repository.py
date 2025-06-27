from sqlalchemy.orm import Session

from models.exam import Exam
from schemas.exam import ExamIn


class ExamRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bulk(self, exams: list[ExamIn]) -> list[Exam]:
        objects = [Exam(**e.dict()) for e in exams]
        self.db.add_all(objects)
        self.db.commit()
        for obj in objects:
            self.db.refresh(obj)
        return objects
