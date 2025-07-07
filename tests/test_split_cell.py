import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.importer.constants import split_cell


def test_split_cell_basic():
    assert split_cell("Н/5") == ["Н", "5"]


def test_split_cell_empty():
    assert split_cell("") == []


def test_split_cell_duplicates():
    assert split_cell("5/5/Н") == ["5", "5", "Н"]


def test_split_cell_space_separator():
    assert split_cell("О 2") == ["О", "2"]


def test_split_cell_multiple_spaces():
    assert split_cell("4  3") == ["4", "3"]
