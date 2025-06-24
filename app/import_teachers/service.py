from __future__ import annotations

import pandas as pd
import structlog
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import (
    Class,
    ClassTeacher,
    ClassTeacherRole,
    Subject,
    Teacher,
    TeacherSubject,
)

logger = structlog.get_logger(__name__)


class ImportReport(BaseModel):
    teachers_created: int = 0
    subjects_created: int = 0
    classes_created: int = 0
    teacher_subjects_created: int = 0
    class_teachers_created: int = 0


class ImportError(BaseModel):
    row: int
    error: str


def _parse_list(value: str | float | None) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    return [v.strip() for v in str(value).split(",") if v and v.strip()]


def _handle_row(
    row: pd.Series,
    db: Session,
    caches: dict,
    report: ImportReport,
    school_id: int,
) -> None | list[ImportError]:
    try:
        teacher_name = str(row["ФИО педагога"]).strip()
        homeroom_classes = _parse_list(row["Классный руководитель"])
        subject_name = str(row["Предмет"]).strip()
        regular_classes = _parse_list(row["Класс"])

        teacher_cache = caches.setdefault("teachers", {})
        subject_cache = caches.setdefault("subjects", {})
        class_cache = caches.setdefault("classes", {})
        ts_cache = caches.setdefault("teacher_subjects", set())
        ct_cache = caches.setdefault("class_teachers", set())

        teacher = teacher_cache.get(teacher_name)
        if teacher is None:
            teacher = (
                db.query(Teacher)
                .filter_by(full_name=teacher_name, school_id=school_id)
                .first()
            )
            if teacher is None:
                teacher = Teacher(full_name=teacher_name, school_id=school_id)
                db.add(teacher)
                report.teachers_created += 1
            teacher_cache[teacher_name] = teacher

        subject = subject_cache.get(subject_name)
        if subject is None:
            subject = (
                db.query(Subject)
                .filter_by(name=subject_name, school_id=school_id)
                .first()
            )
            if subject is None:
                subject = Subject(name=subject_name, school_id=school_id)
                db.add(subject)
                report.subjects_created += 1
            subject_cache[subject_name] = subject

        if (teacher_name, subject_name) not in ts_cache:
            exists = (
                db.query(TeacherSubject)
                .filter_by(teacher_id=teacher.id, subject_id=subject.id)
                .first()
            )
            if not exists:
                db.add(TeacherSubject(teacher=teacher, subject=subject))
                report.teacher_subjects_created += 1
            ts_cache.add((teacher_name, subject_name))

        all_labels = set(homeroom_classes + regular_classes)
        for label in all_labels:
            school_class = class_cache.get(label)
            if school_class is None:
                school_class = (
                    db.query(Class).filter_by(name=label, school_id=school_id).first()
                )
                if school_class is None:
                    school_class = Class(name=label, school_id=school_id)
                    db.add(school_class)
                    report.classes_created += 1
                class_cache[label] = school_class

        for label in regular_classes:
            sc = class_cache[label]
            key = (sc.id, teacher.id, "regular")
            if key not in ct_cache:
                exists = (
                    db.query(ClassTeacher)
                    .filter_by(
                        class_id=sc.id,
                        teacher_id=teacher.id,
                        role=ClassTeacherRole.regular,
                    )
                    .first()
                )
                if not exists:
                    db.add(
                        ClassTeacher(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            role=ClassTeacherRole.regular,
                        )
                    )
                    report.class_teachers_created += 1
                ct_cache.add(key)

        for label in homeroom_classes:
            sc = class_cache[label]
            key = (sc.id, teacher.id, "homeroom")
            if key not in ct_cache:
                existing_homeroom = (
                    db.query(ClassTeacher)
                    .filter_by(class_id=sc.id, role=ClassTeacherRole.homeroom)
                    .first()
                )
                if existing_homeroom and existing_homeroom.teacher_id != teacher.id:
                    return [ImportError(row=int(row.name), error="homeroom conflict")]
                exists = (
                    db.query(ClassTeacher)
                    .filter_by(
                        class_id=sc.id,
                        teacher_id=teacher.id,
                        role=ClassTeacherRole.homeroom,
                    )
                    .first()
                )
                if not exists:
                    db.add(
                        ClassTeacher(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            role=ClassTeacherRole.homeroom,
                        )
                    )
                    report.class_teachers_created += 1
                ct_cache.add(key)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("row processing error", row=int(row.name))
        return [ImportError(row=int(row.name), error=str(exc))]
    return None


def import_teachers_from_file(
    path: str,
    db: Session,
    *,
    dry_run: bool = False,
    truncate_associations: bool = False,
    school_id: int = 1,
) -> ImportReport:
    df = pd.read_excel(path, sheet_name="Справочник педагоги", header=2).ffill()
    report = ImportReport()
    caches: dict = {}

    if truncate_associations:
        db.query(ClassTeacher).delete()
        db.query(TeacherSubject).delete()

    for start in range(0, len(df), 500):
        chunk = df.iloc[start : start + 500]
        for _, row in chunk.iterrows():
            errors = _handle_row(row, db, caches, report, school_id)
            if errors:
                db.rollback()
                raise ValueError(errors[0].error)

    if dry_run:
        db.rollback()
    else:
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            logger.exception("commit failed")
            raise ValueError(str(exc)) from exc

    logger.info("import finished", **report.model_dump())
    return report
