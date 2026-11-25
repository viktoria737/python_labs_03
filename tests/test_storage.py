import json
from pathlib import Path

import pytest

from catalog.manager import Catalog
from catalog.entity import Book
from catalog.exceptions import (
    CorruptedFileError,
    InvalidEntityError,
    UnsupportedVersionError,
)
from catalog.storage import CURRENT_FORMAT_VERSION, load_catalog, save_catalog


def _book(bid="b1") -> Book:
    return Book(book_id=bid, title="Т", category="К", year=2020,
                author="А", isbn="1234567890")


def test_round_trip(tmp_path: Path):
    c = Catalog()
    c.add(_book("b1"))
    c.add(_book("b2"))
    p = tmp_path / "cat.json"
    save_catalog(c, p)

    c2 = load_catalog(p)
    assert len(c2) == 2
    assert [b.book_id for b in c2] == ["b1", "b2"]


def test_format_version_in_root(tmp_path: Path):
    c = Catalog()
    c.add(_book())
    p = tmp_path / "cat.json"
    save_catalog(c, p)
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["format_version"] == CURRENT_FORMAT_VERSION


def test_corrupted_json_does_not_touch_existing(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text("{not a json", encoding="utf-8")

    existing = Catalog()
    existing.add(_book("a"))

    with pytest.raises(CorruptedFileError):
        load_catalog(p)
    assert len(existing) == 1


def test_unknown_version(tmp_path: Path):
    p = tmp_path / "v.json"
    p.write_text(
        json.dumps({"format_version": 9999, "items": []}),
        encoding="utf-8",
    )
    with pytest.raises(UnsupportedVersionError):
        load_catalog(p)


def test_invalid_entity_in_file(tmp_path: Path):
    p = tmp_path / "bad.json"
    payload = {
        "format_version": CURRENT_FORMAT_VERSION,
        "items": [
            {"book_id": "", "title": "T", "category": "C",
             "year": 2020, "author": "A", "isbn": "1234567890"},
        ],
    }
    p.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidEntityError):
        load_catalog(p)


def test_duplicate_in_file_rejected(tmp_path: Path):
    p = tmp_path / "dup.json"
    item = {"book_id": "x", "title": "T", "category": "C",
            "year": 2020, "author": "A", "isbn": "1234567890"}
    payload = {"format_version": CURRENT_FORMAT_VERSION, "items": [item, item]}
    p.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidEntityError):
        load_catalog(p)