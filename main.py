"""Демонстрационный запуск каталога."""

from pathlib import Path

from catalog import Book, Catalog, load_catalog, save_catalog


def main() -> None:
    catalog = Catalog()

    catalog.add(Book(
        book_id="b1",
        title="Война и мир",
        category="Роман",
        year=1869,
        author="Лев Толстой",
        isbn="978-5-17-090123-4",
    ))
    catalog.add(Book(
        book_id="b2",
        title="Мастер и Маргарита",
        category="Роман",
        year=1967,
        author="Михаил Булгаков",
        isbn="978-5-17-082935-1",
    ))
    catalog.add(Book(
        book_id="b3",
        title="Евгений Онегин",
        category="Поэзия",
        year=1833,
        author="Александр Пушкин",
        isbn="978-5-04-097156-2",
    ))

    print(f"Всего книг: {len(catalog)}")
    print("Поиск по имени 'мастер':")
    for b in catalog.find_by_name("мастер"):
        print(f"  - {b.title} ({b.year})")

    print("Поиск по категории 'роман':")
    for b in catalog.find_by_category("роман"):
        print(f"  - {b.title}")

    path = Path("catalog.json")
    save_catalog(catalog, path)
    print(f"Каталог сохранён в {path}")

    loaded = load_catalog(path)
    print(f"Загружено книг: {len(loaded)}")


if __name__ == "__main__":
    main()