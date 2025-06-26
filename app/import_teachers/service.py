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
    ClassTeacherRoleAssociation,
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
    teachers_deleted: int = 0
    ts_deleted: int = 0
    ct_deleted: int = 0


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
        # if a teacher is homeroom for a class, we don't create an additional
        # regular association for the same class
        regular_classes = [
            c for c in regular_classes if c not in homeroom_classes]

        teacher_cache = caches.setdefault("teachers", {})
        subject_cache = caches.setdefault("subjects", {})
        class_cache = caches.setdefault("classes", {})
        ts_cache = caches.setdefault("teacher_subjects", set())
        ct_cache = caches.setdefault("class_teachers", set())
        ts_seen = caches.setdefault("ts_seen", set())
        ct_seen = caches.setdefault("ct_seen", set())
        teachers_seen = caches.setdefault("teachers_seen", set())
        classes_seen = caches.setdefault("classes_seen", set())

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
                db.flush([teacher])
                report.teachers_created += 1
            teacher_cache[teacher_name] = teacher
        teachers_seen.add(teacher_name)

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
                db.flush([subject])
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
                db.flush()
                report.teacher_subjects_created += 1
            ts_cache.add((teacher_name, subject_name, academic_year_id))
        ts_seen.add((teacher_name, subject_name))

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
                    db.flush([school_class])
                    report.classes_created += 1
                class_cache[label] = school_class
            classes_seen.add(label)

        for label in regular_classes:
            sc = class_cache[label]
            key = (sc.id, teacher.id, academic_year_id, "regular")
            if key not in ct_cache:
                exists = (
                    db.query(ClassTeacherRoleAssociation)
                    .filter_by(
                        class_id=sc.id,
                        teacher_id=teacher.id,
                        academic_year_id=academic_year_id,
                        role=ClassTeacherRole.regular,
                    )
                    .first()
                )
                if not exists:
                    ct = (
                        db.query(ClassTeacher)
                        .filter_by(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                        )
                        .first()
                    )
                    if ct is None:
                        ct = ClassTeacher(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                        )
                        db.add(ct)
                        db.flush([ct])
                    db.add(
                        ClassTeacherRoleAssociation(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                            role=ClassTeacherRole.regular,
                        )
                    )
                    db.flush()
                    report.class_teachers_created += 1
                ct_cache.add(key)
            ct_seen.add((sc.name, teacher_name))

        for label in homeroom_classes:
            sc = class_cache[label]
            key = (sc.id, teacher.id, academic_year_id, "homeroom")
            if key not in ct_cache:
                existing_homeroom = (
                    db.query(ClassTeacherRoleAssociation)
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
                    db.query(ClassTeacherRoleAssociation)
                    .filter_by(
                        class_id=sc.id,
                        teacher_id=teacher.id,
                        academic_year_id=academic_year_id,
                        role=ClassTeacherRole.homeroom,
                    )
                    .first()
                )
                if not exists:
                    ct = (
                        db.query(ClassTeacher)
                        .filter_by(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                        )
                        .first()
                    )
                    if ct is None:
                        ct = ClassTeacher(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                        )
                        db.add(ct)
                        db.flush([ct])
                    db.add(
                        ClassTeacherRoleAssociation(
                            class_id=sc.id,
                            teacher_id=teacher.id,
                            academic_year_id=academic_year_id,
                            role=ClassTeacherRole.homeroom,
                        )
                    )
                    db.flush()
                    report.class_teachers_created += 1
                ct_cache.add(key)
            ct_seen.add((sc.name, teacher_name))
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
    header_df = pd.read_excel(
        path, sheet_name="Справочник педагоги", nrows=2, header=None)
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

    df = pd.read_excel(path, sheet_name="Справочник педагоги", header=2)
    # only teacher names may span multiple rows, do not forward fill other columns
    df["ФИО педагога"] = df["ФИО педагога"].ffill()
    teachers_in_file = set(df["ФИО педагога"].dropna().map(str.strip))
    classes_in_file: set[str] = set()
    for _, r in df.iterrows():
        classes_in_file.update(_parse_list(r.get("Класс", None)))
        classes_in_file.update(_parse_list(r.get("Классный руководитель", None)))
    report = ImportReport()
    caches: dict = {}

    if truncate_associations:
        class_ids = [
            cid
            for (cid,) in db.query(Class.id).filter_by(
                school_id=school.id,
                academic_year_id=academic_year.id,
            ).all()
        ]
        if class_ids:
            db.query(ClassTeacher).filter(
                ClassTeacher.class_id.in_(class_ids),
                ClassTeacher.academic_year_id == academic_year.id,
            ).delete(synchronize_session=False)

        teacher_ids = [
            tid for (tid,) in db.query(Teacher.id).filter_by(school_id=school.id).all()
        ]
        if teacher_ids:
            db.query(TeacherSubject).filter(
                TeacherSubject.teacher_id.in_(teacher_ids),
                TeacherSubject.academic_year_id == academic_year.id,
            ).delete(synchronize_session=False)

    for start in range(0, len(df), 500):
        chunk = df.iloc[start: start + 500]
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

    # deletion of entities not present in the new file
    teachers_seen = caches.get("teachers_seen", set())
    ts_seen = caches.get("ts_seen", set())
    ct_seen = caches.get("ct_seen", set())
    classes_seen = caches.get("classes_seen", set())

    # remove teacher subjects
    existing_ts = (
        db.query(TeacherSubject)
        .join(Teacher)
        .join(Subject)
        .filter(Teacher.school_id == school.id)
        .filter(TeacherSubject.academic_year_id == academic_year.id)
        .all()
    )
    for ts in existing_ts:
        key = (ts.teacher.full_name, ts.subject.name)
        if key not in ts_seen:
            report.ts_deleted += 1
            if not dry_run:
                db.delete(ts)

    # remove class teachers
    existing_ct = (
        db.query(ClassTeacher)
        .join(Class)
        .join(Teacher)
        .filter(Class.school_id == school.id)
        .filter(ClassTeacher.academic_year_id == academic_year.id)
        .all()
    )
    for ct in existing_ct:
        pair = (ct.school_class.name, ct.teacher.full_name)
        if pair not in ct_seen:
            report.ct_deleted += 1
            if not dry_run:
                db.delete(ct)

    # remove teachers not present
    if teachers_in_file:
        to_delete = (
            db.query(Teacher)
            .filter(Teacher.school_id == school.id)
            .filter(~Teacher.full_name.in_(teachers_in_file))
            .all()
        )
    else:
        to_delete = db.query(Teacher).filter_by(school_id=school.id).all()
    for teacher in to_delete:
        report.teachers_deleted += 1
        if not dry_run:
            db.delete(teacher)

    # remove classes not present
    existing_classes = (
        db.query(Class)
        .filter_by(school_id=school.id, academic_year_id=academic_year.id)
        .all()
    )
    for cl in existing_classes:
        if cl.name not in classes_seen:
            if not dry_run and len(cl.students) == 0:
                db.delete(cl)
            else:
                if not dry_run:
                    cl.is_archived = True

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
