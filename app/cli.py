# app\import_teachers\cli.py
import argparse
from typing import Any

from app.import_teachers.service import ImportReport, import_teachers_from_file
from backend.core.db import SessionLocal


def _print_report(report: ImportReport) -> None:
    header = f"{'Entity':20}{'Create':>8}{'Update':>8}{'Delete':>8}"
    print(header)
    rows = [
        ("Teachers", report.teachers_created, report.teachers_updated, report.teachers_deleted),
        ("Subjects", report.subjects_created, report.subjects_updated, report.subjects_deleted),
        ("Classes", report.classes_created, report.classes_updated, report.classes_deleted),
        (
            "Teacher subjects",
            report.teacher_subjects_created,
            report.teacher_subjects_updated,
            report.teacher_subjects_deleted,
        ),
        (
            "Class teachers",
            report.class_teachers_created,
            report.class_teachers_updated,
            report.class_teachers_deleted,
        ),
    ]
    for name, c, u, d in rows:
        print(f"{name:20}{c:8}{u:8}{d:8}")
    if report.homeroom_reassigned:
        print(f"homeroom_reassigned: {report.homeroom_reassigned}")


def main(argv: list[str] | None = None) -> Any:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    imp = sub.add_parser("teachers-import")
    imp.add_argument("file")
    imp.add_argument("--dry-run", action="store_true")
    imp.add_argument("--truncate-associations", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "teachers-import":
        db = SessionLocal()
        try:
            report = import_teachers_from_file(
                args.file,
                db,
                dry_run=args.dry_run,
                truncate_associations=args.truncate_associations,
            )
            _print_report(report)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error: {exc}")
            return 1
        finally:
            db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
