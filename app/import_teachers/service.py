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
    teachers_updated: int = 0
    teachers_deleted: int = 0

    subjects_created: int = 0
    subjects_updated: int = 0
    subjects_deleted: int = 0

    classes_created: int = 0
    classes_updated: int = 0
    classes_deleted: int = 0

    teacher_subjects_created: int = 0
    teacher_subjects_updated: int = 0
    teacher_subjects_deleted: int = 0

    class_teachers_created: int = 0
    class_teachers_updated: int = 0
    class_teachers_deleted: int = 0

    homeroom_reassigned: int = 0


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
        regular_classes = [c for c in regular_classes if c not in homeroom_classes]

        teacher_cache = caches.setdefault("teachers", {})
        subject_cache = caches.setdefault("subjects", {})
        class_cache = caches.setdefault("classes", {})
        ts_new = caches.setdefault("ts_new", {})
        ct_new = caches.setdefault("ct_new", {})
        homeroom_map = caches.setdefault("file_homerooms", {})
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

        ts_new.setdefault(teacher.id, set()).add(subject.id)

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
            ct_new.setdefault((sc.id, teacher.id), set()).add(ClassTeacherRole.regular)
            classes_seen.add(label)

        for label in homeroom_classes:
            sc = class_cache[label]
            other = homeroom_map.get(sc.id)
            if other is not None and other != teacher.id:
                return [ImportError(row=int(row.name), error="homeroom conflict")]
            homeroom_map[sc.id] = teacher.id
            ct_new.setdefault((sc.id, teacher.id), set()).add(ClassTeacherRole.homeroom)
            classes_seen.add(label)
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
        path, sheet_name="Справочник педагоги", nrows=2, header=None
    )
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
            for (cid,) in db.query(Class.id)
            .filter_by(
                school_id=school.id,
                academic_year_id=academic_year.id,
            )
            .all()
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
        chunk = df.iloc[start : start + 500]
        chunk_len = len(chunk)
        if chunk_len > 500:
            logger.warning("chunk size exceeded", length=chunk_len)
        assert chunk_len <= 500
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

    # check existing homerooms and handle conflicts or reassignment
    if not truncate_associations:
        file_homerooms: dict[int, int] = caches.get("file_homerooms", {})
        if file_homerooms:
            existing_homerooms = {
                c.class_id: c.teacher_id
                for c in (
                    db.query(ClassTeacherRoleAssociation)
                    .join(Class)
                    .filter(Class.school_id == school.id)
                    .filter(
                        ClassTeacherRoleAssociation.academic_year_id == academic_year.id
                    )
                    .filter(
                        ClassTeacherRoleAssociation.role == ClassTeacherRole.homeroom
                    )
                    .all()
                )
            }
            ct_new: dict[tuple[int, int], set[ClassTeacherRole]] = caches.get(
                "ct_new", {}
            )
            for class_id, new_teacher_id in file_homerooms.items():
                old_teacher_id = existing_homerooms.get(class_id)
                if old_teacher_id is not None and old_teacher_id != new_teacher_id:
                    old_roles = ct_new.get((class_id, old_teacher_id))
                    if old_roles is None:
                        db.rollback()
                        raise ValueError("homeroom conflict")
                    old_roles.discard(ClassTeacherRole.homeroom)
                    report.homeroom_reassigned += 1

    # diff update of associations when not truncating
    if not truncate_associations:
        teacher_cache: dict[str, Teacher] = caches.get("teachers", {})
        subject_cache: dict[str, Subject] = caches.get("subjects", {})
        class_cache: dict[str, Class] = caches.get("classes", {})
        ts_new: dict[int, set[int]] = caches.get("ts_new", {})
        ct_new: dict[tuple[int, int], set[ClassTeacherRole]] = caches.get("ct_new", {})

        teacher_name_by_id = {t.id: name for name, t in teacher_cache.items()}
        subject_name_by_id = {s.id: name for name, s in subject_cache.items()}
        class_name_by_id = {c.id: name for name, c in class_cache.items()}

        # existing teacher-subject relations for this year
        existing_ts = (
            db.query(TeacherSubject)
            .join(Teacher)
            .filter(Teacher.school_id == school.id)
            .filter(TeacherSubject.academic_year_id == academic_year.id)
            .all()
        )
        existing_ts_by_teacher: dict[int, list[TeacherSubject]] = {}
        for ts in existing_ts:
            existing_ts_by_teacher.setdefault(ts.teacher_id, []).append(ts)

        ts_seen: set[tuple[str, str]] = set()

        for teacher_id, subjects in ts_new.items():
            old_list = existing_ts_by_teacher.get(teacher_id, []).copy()
            old_map = {ts.subject_id: ts for ts in old_list}
            unmatched = list(old_list)
            for sub_id in subjects:
                if sub_id in old_map:
                    ts_seen.add(
                        (teacher_name_by_id[teacher_id], subject_name_by_id[sub_id])
                    )
                    unmatched.remove(old_map[sub_id])
                else:
                    if unmatched:
                        ts_to_update = unmatched.pop(0)
                        ts_to_update.subject_id = sub_id
                        report.teacher_subjects_updated += 1
                    else:
                        db.add(
                            TeacherSubject(
                                teacher_id=teacher_id,
                                subject_id=sub_id,
                                academic_year_id=academic_year.id,
                            )
                        )
                        report.teacher_subjects_created += 1
                    ts_seen.add(
                        (teacher_name_by_id[teacher_id], subject_name_by_id[sub_id])
                    )

        caches["ts_seen"] = ts_seen

        # existing class-teacher relations
        existing_ct = (
            db.query(ClassTeacher)
            .join(Class)
            .join(Teacher)
            .filter(Class.school_id == school.id)
            .filter(ClassTeacher.academic_year_id == academic_year.id)
            .all()
        )
        existing_ct_by_pair: dict[tuple[int, int], dict] = {}
        for ct in existing_ct:
            role_map = {r.role: r for r in ct.roles}
            existing_ct_by_pair[(ct.class_id, ct.teacher_id)] = {
                "ct": ct,
                "roles": role_map,
            }

        ct_seen: set[tuple[str, str]] = set()

        # first update/delete existing pairs
        for pair, data in existing_ct_by_pair.items():
            new_roles = ct_new.get(pair)
            class_id, teacher_id = pair
            role_map = data["roles"]
            old_roles = set(role_map.keys())
            if not new_roles:
                # remove roles to avoid conflicts; ct will be deleted later
                for r in role_map.values():
                    db.delete(r)
                continue
            ct_seen.add((class_name_by_id[class_id], teacher_name_by_id[teacher_id]))
            if new_roles != old_roles:
                if len(old_roles) == 1 and len(new_roles) == 1:
                    role_obj = next(iter(role_map.values()))
                    new_val = next(iter(new_roles))
                    if role_obj.role != new_val:
                        role_obj.role = new_val
                        report.class_teachers_updated += 1
                else:
                    for r in old_roles - new_roles:
                        db.delete(role_map[r])
                    for r in new_roles - old_roles:
                        db.add(
                            ClassTeacherRoleAssociation(
                                class_id=class_id,
                                teacher_id=teacher_id,
                                academic_year_id=academic_year.id,
                                role=r,
                            )
                        )
                    report.class_teachers_updated += 1

        # now add completely new pairs
        for pair, roles in ct_new.items():
            if pair in existing_ct_by_pair:
                continue
            class_id, teacher_id = pair
            ct = ClassTeacher(
                class_id=class_id,
                teacher_id=teacher_id,
                academic_year_id=academic_year.id,
            )
            db.add(ct)
            for r in roles:
                db.add(
                    ClassTeacherRoleAssociation(
                        class_id=class_id,
                        teacher_id=teacher_id,
                        academic_year_id=academic_year.id,
                        role=r,
                    )
                )
            report.class_teachers_created += len(roles)
            ct_seen.add((class_name_by_id[class_id], teacher_name_by_id[teacher_id]))

        caches["ct_seen"] = ct_seen

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
            report.teacher_subjects_deleted += 1
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
            report.class_teachers_deleted += 1
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
            report.classes_deleted += 1
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
