from __future__ import annotations

from typing import Iterable, Sequence

import structlog

from pydantic import BaseModel

from sqlalchemy import tuple_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from backend.schemas.grade import GradeCreate
from backend.schemas.attendance import AttendanceCreate
from models.grade import Grade
from models.attendance import Attendance

from .base import BaseParser
from .constants import ImportSummary

log = structlog.get_logger(__name__)


class ImportReport(BaseModel):
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: list[str] = []

    @classmethod
    def from_summary(cls, summary: ImportSummary) -> "ImportReport":
        return cls(**summary.__dict__)


class ImportService:
    """Bulk import grades and attendance records."""

    def __init__(self, db: Session, *, dry_run: bool = False) -> None:
        self.db = db
        self.dry_run = dry_run

    def _upsert_grades(self, grades: Sequence[GradeCreate]) -> ImportSummary:
        summary = ImportSummary()
        if not grades:
            return summary

        values = [g.model_dump() for g in grades]
        keys = [
            (
                g.student_id,
                g.subject_id,
                g.term_type,
                g.term_index,
                g.grade_kind,
                g.lesson_event_id,
            )
            for g in grades
        ]
        existing = set(
            self.db.query(
                Grade.student_id,
                Grade.subject_id,
                Grade.term_type,
                Grade.term_index,
                Grade.grade_kind,
                Grade.lesson_event_id,
            )
            .filter(
                tuple_(
                    Grade.student_id,
                    Grade.subject_id,
                    Grade.term_type,
                    Grade.term_index,
                    Grade.grade_kind,
                    Grade.lesson_event_id,
                ).in_(keys)
            )
            .all()
        )
        for key in keys:
            if key in existing:
                summary.updated += 1
            else:
                summary.created += 1

        if not self.dry_run:
            stmt = insert(Grade).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=[
                    Grade.student_id,
                    Grade.subject_id,
                    Grade.term_type,
                    Grade.term_index,
                    Grade.grade_kind,
                    Grade.lesson_event_id,
                ],
                set_={"value": stmt.excluded.value},
            )
            self.db.execute(stmt)
        return summary

    def _upsert_attendance(self, records: Sequence[AttendanceCreate]) -> ImportSummary:
        summary = ImportSummary()
        if not records:
            return summary

        values = [r.model_dump() for r in records]
        keys = [(r.student_id, r.date) for r in records]
        existing = set(
            self.db.query(Attendance.student_id, Attendance.date)
            .filter(tuple_(Attendance.student_id, Attendance.date).in_(keys))
            .all()
        )
        for key in keys:
            if key in existing:
                summary.updated += 1
            else:
                summary.created += 1

        if not self.dry_run:
            stmt = insert(Attendance).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=[Attendance.student_id, Attendance.date],
                set_={
                    "status": stmt.excluded.status,
                    "minutes_late": stmt.excluded.minutes_late,
                },
            )
            self.db.execute(stmt)
        return summary

    def import_items(self, items: Iterable[object]) -> ImportSummary:
        summary = ImportSummary()
        grades: list[GradeCreate] = []
        attendance: list[AttendanceCreate] = []
        for item in items:
            if isinstance(item, GradeCreate):
                grades.append(item)
            elif isinstance(item, AttendanceCreate):
                attendance.append(item)
        summary += self._upsert_grades(grades)
        summary += self._upsert_attendance(attendance)
        if self.dry_run:
            self.db.rollback()
        else:
            self.db.commit()
        return summary

    def import_from_parser(self, parser: BaseParser) -> ImportSummary:
        summary = ImportSummary()
        for batch in parser.iter_batches():
            try:
                batch_summary = self.import_items(batch)
            except Exception:  # pylint: disable=broad-except
                log.error("import_error", exc_info=True)
                raise
            else:
                log.info(
                    "batch_imported",
                    created=batch_summary.created,
                    updated=batch_summary.updated,
                    skipped=batch_summary.skipped,
                )
                summary += batch_summary
        return summary
