import pandas as pd
from sqlalchemy.orm import Session

from models import Subject
from repositories.subject_alias_repository import SubjectAliasRepository
from backend.services import resolve_subject


def import_aliases_from_file(path: str, db: Session) -> int:
    """Import subject aliases from CSV or XLSX file.

    Expected columns: alias, subject
    Returns number of aliases imported.
    """
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    elif path.lower().endswith(".xlsx"):
        df = pd.read_excel(path)
    else:
        raise ValueError("unsupported file format")

    repo = SubjectAliasRepository(db)
    count = 0
    for _, row in df.iterrows():
        alias = str(row.get("alias") or row.get("Alias") or row[0]).strip()
        subject_name = str(row.get("subject") or row.get("Subject") or row[1]).strip()
        if not alias or not subject_name:
            continue
        subject = resolve_subject(db, subject_name)
        if subject is None:
            continue
        if repo.get_by_alias(alias) is None:
            repo.create(alias, subject)
            count += 1
    return count

