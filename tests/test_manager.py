import pytest

from catalog.manager import Catalog
from catalog.entity import Book
from catalog.exceptions import DuplicateIdError, NotFoundError


def _book(bid="b1", title="Книга", category="Роман", year=2000,
          author="Автор", isbn="1234567890") -> Book:
    return Book(book_id=bid, title=title, category=category,
                year=year, author=author, isbn=isbn)


def test_add_get_remove():
    c = Catalog()
    b = _book()
    c.add(b)
    assert c.get("b1") is b
    c.remove("b1")
    with pytest.raises(NotFoundError):
        c.get("b1")


def test_duplicate_id_rejected():
    c = Catalog()
    c.add(_book(bid="x"))
    with pytest.raises(DuplicateIdError):
        c.add(_book(bid="x"))


def test_remove_missing_raises():
    c = Catalog()
    with pytest.raises(NotFoundError):
        c.remove("no")


def test_find_by_category():
    c = Catalog()
    c.add(_book(bid="1", category="Роман"))
    c.add(_book(bid="2", category="роман"))
    c.add(_book(bid="3", category="Поэзия"))
    res = c.find_by_category("РОМАН")
    assert {b.book_id for b in res} == {"1", "2"}


def test_find_by_name_case_insensitive():
    c = Catalog()
    c.add(_book(bid="1", title="Мастер и Маргарита"))
    c.add(_book(bid="2", title="Мастер"))
    c.add(_book(bid="3", title="Другое"))
    res = c.find_by_name("мастер")
    assert {b.book_id for b in res} == {"1", "2"}


def test_find_by_name_returns_new_list():
    c = Catalog()
    c.add(_book(bid="1", title="А"))
    a = c.find_by_name("А")
    b = c.find_by_name("А")
    assert a is not b


def test_iteration_order_deterministic():
    c = Catalog()
    ids = ["a", "b", "c", "d"]
    for i in ids:
        c.add(_book(bid=i))
    assert [b.book_id for b in c] == ids
    assert [b.book_id for b in c] == ids


def test_len_and_contains():
    c = Catalog()
    assert len(c) == 0
    c.add(_book(bid="x"))
    assert len(c) == 1
    assert "x" in c
    assert "y" not in c