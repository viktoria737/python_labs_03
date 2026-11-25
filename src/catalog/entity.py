from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict

from .exceptions import InvalidEntityError

CURRENT_YEAR = date.today().year

@dataclass(frozen=True)
class Book:
    book_id: str
    title: str
    category: str
    year: int
    author: str
    isbn: str

    def __post_init__(self) -> None:
        self._validate_id(self.book_id)
        self._validate_title(self.title)
        self._validate_category(self.category)
        self._validate_year(self.year)
        self._validate_author(self.author)
        self._validate_isbn(self.isbn)

    @staticmethod
    def _validate_id(value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidEntityError("Идентификатор должен быть непустой строкой")

    @staticmethod
    def _validate_title(value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidEntityError("Название должно быть непустой строкой")

    @staticmethod
    def _validate_category(value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidEntityError("Категория должна быть непустой строкой")

    @staticmethod
    def _validate_year(value: Any) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidEntityError("Год должен быть целым числом")
        if not (1000 <= value <= CURRENT_YEAR):
            raise InvalidEntityError(
                f"Год должен быть в диапазоне [1000; {CURRENT_YEAR}]"
            )

    @staticmethod
    def _validate_author(value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidEntityError("Автор должен быть непустой строкой")

    @staticmethod
    def _validate_isbn(value: Any) -> None:
        if not isinstance(value, str):
            raise InvalidEntityError("ISBN должен быть строкой")
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) not in (10, 13):
            raise InvalidEntityError(
                "ISBN должен содержать 10 или 13 цифр (дефисы/пробелы допустимы)"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "category": self.category,
            "year": self.year,
            "author": self.author,
            "isbn": self.isbn,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            category=data["category"],
            year=data["year"],
            author=data["author"],
            isbn=data["isbn"],
        )