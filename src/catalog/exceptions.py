class CatalogError(Exception):
    """Базовое исключение для всех ошибок каталога."""


class InvalidEntityError(CatalogError):
    """Сущность не прошла проверку инвариантов."""


class DuplicateIdError(CatalogError):
    """Попытка добавить объект с уже существующим ID."""


class NotFoundError(CatalogError):
    """Объект с указанным ID не найден."""


class UnsupportedVersionError(CatalogError):
    """Неподдерживаемая версия формата"""


class CorruptedFileError(CatalogError):
    """Файл повреждён или не является валидным JSON."""