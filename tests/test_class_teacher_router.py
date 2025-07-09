import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "x")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "db")
os.environ.setdefault("DB_USER", "user")
os.environ.setdefault("DB_PASSWORD", "pass")

from backend.routers.class_teacher_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_assign_requires_authentication():
    payload = {
        "class_id": 1,
        "teacher_id": 1,
        "academic_year_id": 1,
        "role": "regular",
    }
    resp = client.post("/class-teachers/", json=payload)
    assert resp.status_code == 401
