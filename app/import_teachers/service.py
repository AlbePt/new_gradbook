# app\import_teachers\service.py
from __future__ import annotations

import pandas as pd
import structlog
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from datetime import date
import re

from models import (
    AcademicYear,
    Class,
    ClassTeacher,
    ClassTeacherRole,
    School,
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
    academic_year_id: int,
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

        if (teacher_name, subject_name, academic_year_id) not in ts_cache:
            exists = (
                db.query(TeacherSubject)
                .filter_by(
                    teacher_id=teacher.id,
                    subject_id=subject.id,
                    academic_year_id=academic_year_id,
                )
                .first()
            )
            if not exists:
                db.add(
                    TeacherSubject(
                        teacher=teacher,
                        subject=subject,
                        academic_year_id=academic_year_id,
                    )
                )
                report.teacher_subjects_created += 1
            ts_cache.add((teacher_name, subject_name, academic_year_id))

        all_labels = set(homeroom_classes + regular_classes)
        for label in all_labels:
            school_class = class_cache.get(label)
            if school_class is None:
                school_class = (
                    db.query(Class)
                    .filter_by(
                        name=label,
                        school_id=school_id,
                        academic_year_id=academic_year_id,
                    )
                    .first()
                )
                if school_class is None:
                    school_class = Class(
                        name=label,
                        school_id=school_id,
                        academic_year_id=academic_year_id,
                    )
                    db.add(school_class)
                    report.classes_created += 1
                class_cache[label] = school_class

        for label in regular_classes:
            sc = class_cache[label]
            key = (sc.id, teacher.id, academic_year_id, "regular")
            if key not in ct_cache:
                exists = (
                    db.query(ClassTeacher)
                    .filter_by(
                        class_id=sc.id,
                        teacher_id=teacher.id,
                        academic_year_id=academic_year_id,
                        role=ClassTeacherRole.regular,
                    )
                    .first()
                )
                if not exists:
                    db.add(
                        ClassTeacher(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                            role=ClassTeacherRole.regular,
                        )
                    )
                    report.class_teachers_created += 1
                ct_cache.add(key)

        for label in homeroom_classes:
            sc = class_cache[label]
            key = (sc.id, teacher.id, academic_year_id, "homeroom")
            if key not in ct_cache:
                existing_homeroom = (
                    db.query(ClassTeacher)
                    .filter_by(
                        class_id=sc.id,
                        role=ClassTeacherRole.homeroom,
                        academic_year_id=academic_year_id,
                    )
                    .first()
                )
                if existing_homeroom and existing_homeroom.teacher_id != teacher.id:
                    return [ImportError(row=int(row.name), error="homeroom conflict")]
                exists = (
                    db.query(ClassTeacher)
                    .filter_by(
                        class_id=sc.id,
                        teacher_id=teacher.id,
                        academic_year_id=academic_year_id,
                        role=ClassTeacherRole.homeroom,
                    )
                    .first()
                )
                if not exists:
                    db.add(
                        ClassTeacher(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
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
) -> ImportReport:
    header_df = pd.read_excel(path, sheet_name="Справочник педагоги", nrows=2, header=None)
    year_line = str(header_df.iloc[0, 0])
    school_name = str(header_df.iloc[1, 0]).strip()
    m = re.search(r"(\d{4})/(\d{4})", year_line)
    if not m:
        raise ValueError("invalid academic year")
    start_year = int(m.group(1))
    end_year = int(m.group(2))
    year_name = f"{start_year}/{end_year}"

    academic_year = db.query(AcademicYear).filter_by(name=year_name).first()
    if academic_year is None:
        academic_year = AcademicYear(
            name=year_name,
            year_start=date(start_year, 9, 1),
            year_end=date(end_year, 8, 31),
        )
        db.add(academic_year)
        db.flush()

    school = db.query(School).filter_by(full_name=school_name).first()
    if school is None:
        raise ValueError("school not found")

    df = pd.read_excel(path, sheet_name="Справочник педагоги", header=2).ffill()
    report = ImportReport()
    caches: dict = {}

    class_ids = [
        cid for (cid,) in db.query(Class.id).filter_by(
            school_id=school.id,
            academic_year_id=academic_year.id,
        ).all()
    ]
    if class_ids:
        db.query(ClassTeacher).filter(
            ClassTeacher.class_id.in_(class_ids),
            ClassTeacher.academic_year_id == academic_year.id,
        ).delete(synchronize_session=False)

    teacher_ids = [tid for (tid,) in db.query(Teacher.id).filter_by(school_id=school.id).all()]
    if teacher_ids:
        db.query(TeacherSubject).filter(
            TeacherSubject.teacher_id.in_(teacher_ids),
            TeacherSubject.academic_year_id == academic_year.id,
        ).delete(synchronize_session=False)

    for start in range(0, len(df), 500):
        chunk = df.iloc[start : start + 500]
        for _, row in chunk.iterrows():
            errors = _handle_row(
                row,
                db,
                caches,
                report,
                school.id,
                academic_year.id,
            )
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
