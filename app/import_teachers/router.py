# app\import_teachers\router.py
from pathlib import Path
import tempfile
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from backend.core.db import get_db

from .service import import_teachers_from_file

router = APIRouter()


@router.post("/import/teachers")
async def import_teachers_endpoint(
    file: UploadFile = File(...),
    dry_run: bool = Query(False),
    truncate_associations: bool = Query(False),
    db: Session = Depends(get_db),
):
    tmp_dir = Path(tempfile.gettempdir())  
    tmp_path = tmp_dir / f"{uuid4()}.xlsx"
    tmp_path.write_bytes(await file.read())
    try:
        report = import_teachers_from_file(
            str(tmp_path),
            db,
            dry_run=dry_run,
            truncate_associations=truncate_associations,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        tmp_path.unlink(missing_ok=True)
    return {"dry_run": dry_run, **report.model_dump()}
