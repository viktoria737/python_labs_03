from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union

from .manager import Catalog
from .entity import Book
from .exceptions import (
    CatalogError,
    CorruptedFileError,
    InvalidEntityError,
    UnsupportedVersionError,
)

CURRENT_FORMAT_VERSION = 1


def _validate_document(data: Any) -> None:
    if not isinstance(data, dict):
        raise CorruptedFileError("Корень JSON должен быть объектом")
    if "format_version" not in data:
        raise CorruptedFileError("Отсутствует поле format_version")
    if "items" not in data or not isinstance(data["items"], list):
        raise CorruptedFileError("Отсутствует или некорректно поле items")


def save_catalog(catalog: Catalog, path: Union[str, Path]) -> None:
    """Сохраняем каталог в JSON."""
    path = Path(path)
    payload: Dict[str, Any] = {
        "format_version": CURRENT_FORMAT_VERSION,
        "items": [book.to_dict() for book in catalog],
    }
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(path)
    except OSError as e:
        raise CorruptedFileError(f"Не удалось сохранить файл: {e}")


def load_catalog(path: Union[str, Path]) -> Catalog:
    """Загружаем каталог из JSON."""
    path = Path(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise CorruptedFileError(f"Не удалось прочитать файл: {e}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise CorruptedFileError(f"Файл не является валидным JSON: {e}")

    _validate_document(data)

    version = data["format_version"]
    if version != CURRENT_FORMAT_VERSION:
        raise UnsupportedVersionError(f"Неподдерживаемая версия формата: {version} ")

    parsed: list[Book] = []
    for i, item in enumerate(data["items"]):
        try:
            parsed.append(Book.from_dict(item))
        except CatalogError as e:
            raise InvalidEntityError(f"Элемент #{i}: {e}") from e

    catalog = Catalog()
    seen: set[str] = set()
    for book in parsed:
        if book.book_id in seen:
            raise InvalidEntityError(
                f"В файле обнаружен дубликат ID: {book.book_id}"
            )
        seen.add(book.book_id)
        catalog.add(book)
    return catalog