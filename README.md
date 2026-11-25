# Каталог объектов
### Предметная область: библиотечные книги
Пакет с предметной моделью и каталогом объектов.

## Возможности

* Регистронезависимый поиск по категории и названию.
* Поиск по ID.
* Запрет дубликатов ID.
* Детерминированный порядок итерации.
* Сохранение каталога в JSON-файл.
* Загрузка каталога из JSON-файла.

## Ошибки

* Неверная сущность.
* Дубликат ID.
* Объект не найден.
* Неподдерживаемая версия формата.
* Повреждённый файл.

## Установка

Создание виртуального окружения:

```bash
python -m venv .venv
```

Активация окружения:

```bash
#Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\Activate.ps1
```

Установка пакета:

```bash
pip install -e .[dev]
```
## Запуск демонстрации

```bash
python main.py
```

# Структура проекта

```text
lab_03/
|── src/
|   └── catalog/
|       |── __init__.py
|       |── entity.py
|       |── exceptions.py
|       |── manager.py
|       └── storage.py

|── tests/
|   |── __init__.py
|   |── test_entity.py
|   |── test_manager.py
|   └── test_storage.py
|
|── .gitignore
|── main.py
|── pyproject.toml
└── README.md

```