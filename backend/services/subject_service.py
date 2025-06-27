from sqlalchemy.orm import Session

from models import Subject, SubjectAlias


def resolve_subject(db: Session, name: str) -> Subject | None:
    subject = db.query(Subject).filter_by(name=name).first()
    if subject:
        return subject
    alias = db.query(SubjectAlias).filter_by(alias=name).first()
    if alias:
        return alias.subject
    return None

