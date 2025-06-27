from sqlalchemy.orm import Session
from models import SubjectAlias, Subject


class SubjectAliasRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_alias(self, alias: str) -> SubjectAlias | None:
        return self.db.query(SubjectAlias).filter_by(alias=alias).first()

    def create(self, alias: str, subject: Subject) -> SubjectAlias:
        obj = SubjectAlias(alias=alias, subject=subject)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

