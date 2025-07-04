from __future__ import annotations

from typing import Iterable, Sequence, Dict
from datetime import date

import structlog

from pydantic import BaseModel

from sqlalchemy import tuple_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from backend.services import (
    resolve_or_create_class,
    resolve_or_create_student,
    resolve_or_create_year,
    resolve_subject,
)
from models import LessonEvent, School, Teacher, AcademicPeriod
from models.grade import GradeKindEnum, TermTypeEnum
from models.attendance import AttendanceStatusEnum

from backend.schemas.grade import GradeCreate
from backend.schemas.attendance import AttendanceCreate
from models.grade import Grade
from models.attendance import Attendance
from models.academic_year import AcademicYear

from .base import BaseParser, ParsedRow
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

    def __init__(self, db: Session, *, dry_run: bool = False, school_id: int | None = None) -> None:
        self.db = db
        self.dry_run = dry_run
        self._ay_cache: Dict[int, int] = {}
        self._period_cache: Dict[int, list] = {}
        self.school_id = school_id or self._get_default_school_id()

    def _get_default_school_id(self) -> int:
        school = self.db.query(School.id).first()
        if school is None:
            raise ValueError("no school found")
        return school[0]

    def _get_academic_year_id(self, day: date) -> int:
        key = day.year * 100 + day.month  # simple cache key
        cached = self._ay_cache.get(key)
        if cached is not None:
            return cached
        ay = (
            self.db.query(AcademicYear)
            .filter(AcademicYear.year_start <= day)
            .filter(AcademicYear.year_end >= day)
            .first()
        )
        if ay is None:
            raise ValueError(f"academic year not found for {day}")
        self._ay_cache[key] = ay.id
        return ay.id

    def _get_period_info(self, year_id: int, day: date) -> tuple[TermTypeEnum, int] | None:
        """Return term type and index for a date using DB periods."""
        periods = self._period_cache.get(year_id)
        if periods is None:
            periods = (
                self.db.query(AcademicPeriod)
                .filter_by(academic_year_id=year_id)
                .all()
            )
            self._period_cache[year_id] = periods
        for period in periods:
            if period.start_date <= day <= period.end_date:
                return period.term_type, period.term_index
        return None

    def _get_lesson_event_id(
        self,
        day: date,
        subject_id: int,
        class_id: int,
        lesson_index: int | None = None,
    ) -> int:
        query = (
            self.db.query(LessonEvent)
            .filter_by(subject_id=subject_id, class_id=class_id, lesson_date=day)
        )
        if lesson_index is not None:
            query = query.filter_by(lesson_index=lesson_index)
        event = query.first()
        if event is None:
            event = LessonEvent(
                subject_id=subject_id,
                class_id=class_id,
                lesson_date=day,
                lesson_index=lesson_index,
            )
            self.db.add(event)
            self.db.flush([event])
        return event.id

    def _delete_old_regular_grades(
        self,
        keys: Iterable[tuple[int, int, TermTypeEnum, int]],
    ) -> None:
        """Delete existing regular grades for provided combinations."""
        if self.dry_run:
            return
        for class_id, year_id, term_type, term_index in keys:
            (
                self.db.query(Grade)
                .join(LessonEvent)
                .filter(LessonEvent.class_id == class_id)
                .filter(Grade.academic_year_id == year_id)
                .filter(Grade.term_type == term_type)
                .filter(Grade.term_index == term_index)
                .filter(Grade.grade_kind == GradeKindEnum.regular)
                .delete(synchronize_session=False)
            )

    def _upsert_grades(self, grades: Sequence[GradeCreate]) -> ImportSummary:
        summary = ImportSummary()
        if not grades:
            return summary

        items = {}
        for g in grades:
            data = g.model_dump()
            if data.get("academic_year_id") is None:
                data["academic_year_id"] = self._get_academic_year_id(g.date)
            key = (
                g.student_id,
                g.subject_id,
                g.term_type,
                g.term_index,
                g.grade_kind,
                g.lesson_event_id,
            )
            items[key] = data
        keys = list(items.keys())
        values = list(items.values())
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

        items = {}
        for r in records:
            data = r.model_dump()
            if data.get("academic_year_id") is None:
                data["academic_year_id"] = self._get_academic_year_id(r.date)
            key = (r.student_id, r.date)
            items[key] = data
        keys = list(items.keys())
        values = list(items.values())
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

    def import_items(self, items: Iterable[ParsedRow]) -> ImportSummary:
        summary = ImportSummary()
        grades: list[GradeCreate] = []
        attendance: list[AttendanceCreate] = []
        deletions: set[tuple[int, int, TermTypeEnum, int]] = set()
        for row in items:
            year_id = resolve_or_create_year(self.db, row.academic_year_name)
            class_id = resolve_or_create_class(
                self.db, row.class_name, self.school_id, year_id
            )
            student_id = resolve_or_create_student(
                self.db,
                row.student_name,
                self.school_id,
                class_id,
                row.class_name,
            )
            subj = resolve_subject(self.db, row.subject_name)
            if subj is None:
                summary.skipped += 1
                summary.errors.append(f"subject not found: {row.subject_name}")
                continue
            subject_id = subj.id

            teacher_id = None
            if row.teacher_name:
                teacher = (
                    self.db.query(Teacher)
                    .filter_by(full_name=row.teacher_name, school_id=self.school_id)
                    .first()
                )
                if teacher:
                    teacher_id = teacher.id

            event_id = self._get_lesson_event_id(
                row.lesson_date, subject_id, class_id, row.lesson_index
            )

            if row.grade_value is not None:
                period_info = self._get_period_info(year_id, row.lesson_date)
                if period_info:
                    term_type, term_index = period_info
                else:
                    term_type = (
                        TermTypeEnum(row.term_type)
                        if isinstance(row.term_type, str)
                        else row.term_type or TermTypeEnum.year
                    )
                    term_index = row.term_index or 1
                grade_kind = (
                    GradeKindEnum(row.grade_kind)
                    if isinstance(row.grade_kind, str)
                    else row.grade_kind
                )
                if grade_kind == GradeKindEnum.regular:
                    deletions.add((class_id, year_id, term_type, term_index))
                grades.append(
                    GradeCreate(
                        value=row.grade_value,
                        date=row.lesson_date,
                        student_id=student_id,
                        teacher_id=teacher_id,
                        subject_id=subject_id,
                        term_type=term_type,
                        term_index=term_index,
                        grade_kind=grade_kind,
                        lesson_event_id=event_id,
                        academic_year_id=year_id,
                    )
                )

            if row.attendance_status is not None:
                status = (
                    AttendanceStatusEnum(row.attendance_status)
                    if isinstance(row.attendance_status, str)
                    else row.attendance_status
                )
                attendance.append(
                    AttendanceCreate(
                        date=row.lesson_date,
                        status=status,
                        minutes_late=row.minutes_late,
                        comment=row.comment,
                        student_id=student_id,
                        lesson_event_id=event_id,
                        academic_year_id=year_id,
                    )
                )

        self._delete_old_regular_grades(deletions)
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
