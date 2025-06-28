from __future__ import annotations

from enum import Enum
from pathlib import Path
import tempfile
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from backend.core.db import get_db
from .mark_sheet_parser import MarkSheetParser
from .progress_report_parser import ProgressReportParser
from .service import ImportService, ImportReport


class ParserType(str, Enum):
    mark_sheet = "mark_sheet"
    progress_report = "progress_report"


router = APIRouter()


@router.post("/import")
async def import_endpoint(
    parser_type: ParserType = Query(...),
    file: UploadFile = File(...),
    dry_run: bool = Query(False),
    db: Session = Depends(get_db),
):
    tmp_dir = Path(tempfile.gettempdir())
    tmp_path = tmp_dir / f"{uuid4()}.xlsx"
    tmp_path.write_bytes(await file.read())

    try:
        if parser_type is ParserType.mark_sheet:
            parser = MarkSheetParser(str(tmp_path))
        elif parser_type is ParserType.progress_report:
            parser = ProgressReportParser(str(tmp_path))
        else:
            raise HTTPException(status_code=400, detail="unknown parser type")

        service = ImportService(db, dry_run=dry_run)
        summary = service.import_from_parser(parser)
        report = ImportReport.model_validate(summary.__dict__)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        tmp_path.unlink(missing_ok=True)

    return {"dry_run": dry_run, **report.model_dump()}
