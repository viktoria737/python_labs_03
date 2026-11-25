from __future__ import annotations

from typing import Iterator, List

from .entity import Book
from .exceptions import DuplicateIdError, InvalidEntityError, NotFoundError


class Catalog:
    def __init__(self) -> None:
        self._items: dict[str, Book] = {}

    def add(self, item: Book) -> None:
        if not isinstance(item, Book):
            raise InvalidEntityError("Можно добавлять только объекты Book")
        if item.book_id in self._items:
            raise DuplicateIdError(f"Дубликат ID: {item.book_id}")
        self._items[item.book_id] = item

    def get(self, item_id: str) -> Book:
        try:
            return self._items[item_id]
        except KeyError:
            raise NotFoundError(f"Объект с ID '{item_id}' не найден")

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise NotFoundError(f"Объект с ID '{item_id}' не найден")
        del self._items[item_id]

    def find_by_category(self, category: str) -> List[Book]:
        target = category.strip().lower()
        return [b for b in self._items.values() if b.category.lower() == target]

    def find_by_name(self, query: str) -> List[Book]:
        q = query.strip().lower()
        if not q:
            return []
        return [b for b in self._items.values() if q in b.title.lower()]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Book]:
        for book in self._items.values():
            yield book

    def __contains__(self, item_id: object) -> bool:
        return isinstance(item_id, str) and item_id in self._items

    def all_items(self) -> List[Book]:
        return list(self._items.values())