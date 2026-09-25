"""Пути к ресурсам проекта, не зависящие от текущего рабочего каталога."""

from pathlib import Path

#: корень репозитория (src/coworking/paths.py -> parents[2])
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#: каталог со схемой БД
SQL_SCHEMA_DIR = PROJECT_ROOT / "sql" / "schema"

#: файл с данными для заполнения статических таблиц
STATIC_TABLES_FILE = Path(__file__).resolve().parent / "data" / "static_tables.json"

#: файл с параметрами подключения (в .gitignore)
CONNECTION_CONFIG_FILE = PROJECT_ROOT / "connection_config.json"


def sql_schema(*parts: str) -> Path:
    """Путь к файлу внутри sql/schema."""
    return SQL_SCHEMA_DIR.joinpath(*parts)
