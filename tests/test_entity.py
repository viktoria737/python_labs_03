import pytest

from catalog.entity import Book
from catalog.exceptions import InvalidEntityError

VALID = dict(
    book_id="b1",
    title="Война и мир",
    category="Роман",
    year=1869,
    author="Л. Толстой",
    isbn="978-5-17-090123-4",
)


def test_valid_book_creation():
    b = Book(**VALID)
    assert b.book_id == "b1"
    assert b.title == "Война и мир"


def test_empty_id_rejected():
    with pytest.raises(InvalidEntityError):
        Book(**{**VALID, "book_id": ""})


def test_empty_title_rejected():
    with pytest.raises(InvalidEntityError):
        Book(**{**VALID, "title": "   "})


def test_year_too_small_rejected():
    with pytest.raises(InvalidEntityError):
        Book(**{**VALID, "year": 500})


def test_year_in_future_rejected():
    with pytest.raises(InvalidEntityError):
        Book(**{**VALID, "year": 9999})


def test_year_not_int_rejected():
    with pytest.raises(InvalidEntityError):
        Book(**{**VALID, "year": "1869"})


def test_isbn_invalid_length_rejected():
    with pytest.raises(InvalidEntityError):
        Book(**{**VALID, "isbn": "12345"})


def test_isbn_with_hyphens_accepted():
    b = Book(**{**VALID, "isbn": "978-5-17-090123-4"})
    assert b.isbn == "978-5-17-090123-4"


def test_round_trip_dict():
    b = Book(**VALID)
    b2 = Book.from_dict(b.to_dict())
    assert b == b2