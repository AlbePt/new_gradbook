# app\import_teachers\cli.py
import argparse
from typing import Any

import structlog

from app.logging import configure_logging
from app.import_teachers.service import ImportReport, import_teachers_from_file
from app.import_aliases.service import import_aliases_from_file
from app.importer.mark_sheet_parser import MarkSheetParser
from app.importer.progress_report_parser import ProgressReportParser
from app.importer.service import ImportService, ImportReport as GenericReport
from backend.core.db import SessionLocal

log = structlog.get_logger(__name__)


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
    log.info("teachers_import_summary", **report.model_dump())


def main(argv: list[str] | None = None) -> Any:
    configure_logging()

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    imp = sub.add_parser("teachers-import")
    imp.add_argument("file")
    imp.add_argument("--dry-run", action="store_true")
    imp.add_argument("--truncate-associations", action="store_true")

    alias_p = sub.add_parser("import-aliases")
    alias_p.add_argument("file")

    gen = sub.add_parser("import")
    gen.add_argument("parser", choices=["mark_sheet", "progress_report"])
    gen.add_argument("file")
    gen.add_argument("--dry-run", action="store_true")

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
            log.error("teachers_import_error", exc_info=True)
            print(f"Error: {exc}")
            return 1
        finally:
            db.close()
    elif args.cmd == "import-aliases":
        db = SessionLocal()
        try:
            count = import_aliases_from_file(args.file, db)
            print(f"Imported {count} aliases")
            log.info("aliases_imported", count=count)
        except Exception as exc:  # pylint: disable=broad-except
            log.error("aliases_import_error", exc_info=True)
            print(f"Error: {exc}")
            return 1
        finally:
            db.close()
    elif args.cmd == "import":
        db = SessionLocal()
        try:
            if args.parser == "mark_sheet":
                parser_obj = MarkSheetParser(args.file)
            else:
                parser_obj = ProgressReportParser(args.file)

            service = ImportService(db, dry_run=args.dry_run)
            summary = service.import_from_parser(parser_obj)
            report = GenericReport.from_summary(summary)
            log.info("import_finished", parser=args.parser, dry_run=args.dry_run, **report.model_dump())
        except Exception as exc:  # pylint: disable=broad-except
            log.error("import_error", exc_info=True)
            print(f"Error: {exc}")
            return 1
        finally:
            db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
