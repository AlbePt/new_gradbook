from sqlalchemy.orm import Session
from schemas.exam import ExamIn
from repositories.exam_repository import ExamRepository


class ExamService:
    def __init__(self, db: Session):
        self.repo = ExamRepository(db)

    def create_bulk(self, exams: list[ExamIn]):
        return self.repo.create_bulk(exams)
