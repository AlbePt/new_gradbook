import argparse
from typing import Any

from app.import_teachers.service import import_teachers_from_file
from backend.core.db import SessionLocal


def main(argv: list[str] | None = None) -> Any:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    imp = sub.add_parser("import-teachers")
    imp.add_argument("file")
    imp.add_argument("--dry-run", action="store_true")
    imp.add_argument("--truncate-associations", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "import-teachers":
        db = SessionLocal()
        try:
            report = import_teachers_from_file(
                args.file,
                db,
                dry_run=args.dry_run,
                truncate_associations=args.truncate_associations,
            )
            print(report.model_dump())
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error: {exc}")
            return 1
        finally:
            db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
