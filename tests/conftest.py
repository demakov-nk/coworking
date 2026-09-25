"""Общие фикстуры для тестов заданий."""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pytest  # noqa: E402

from coworking.data.loader import load_static_tables  # noqa: E402


def db_available() -> tuple[bool, str]:
    """Проверить, доступна ли БД с параметрами из connection_config.json."""
    try:
        from coworking.db.connection import get_connection
    except ImportError as err:
        return False, f"нет драйвера подключения: {err}"

    try:
        conn = get_connection()
    except Exception as err:  # noqa: BLE001 — psycopg2.errors.OperationalError и т.п.
        return False, f"нет подключения к БД: {err}"

    conn.close()
    return True, ""


@pytest.fixture(scope="session")
def conn():
    ok, reason = db_available()
    if not ok:
        pytest.skip(reason)

    from coworking.db.connection import get_connection

    connection = get_connection()
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def cur(conn):
    cursor = conn.cursor()
    yield cursor
    cursor.close()


@pytest.fixture
def static_data() -> dict:
    return load_static_tables()


@pytest.fixture
def n_genders(static_data) -> int:
    return len(static_data["gender"])


@pytest.fixture
def faker():
    from faker import Faker

    return Faker("ru_RU")


# --- значения по умолчанию для параметров тестов ---------------------------
# совпадают с теми, что использовались в блоках main() этих файлов
@pytest.fixture
def n_clients_to_insert() -> int:
    return 10


@pytest.fixture
def n_clients_to_delete() -> int:
    return 1


@pytest.fixture
def n_clients_to_update(n_clients_to_insert) -> int:
    return n_clients_to_insert


@pytest.fixture
def n_subs_to_insert() -> int:
    return 10


@pytest.fixture
def n_visits_to_insert() -> int:
    return 10


@pytest.fixture
def client_id(cur) -> int:
    """Случайный клиент, у которого есть хотя бы один визит.

    Такой клиент подходит и для тестов абонементов: визит возможен только
    по договору, а договор — только при наличии абонемента.
    """
    from random import choice

    cur.execute("SELECT DISTINCT client_id FROM visit")
    return choice(cur.fetchall())[0]
