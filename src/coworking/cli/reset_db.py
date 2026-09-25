"""Сброс схемы БД и создание её заново."""

from coworking.db.connection import get_connection
from coworking.db.schema import run_sql
from coworking.paths import sql_schema


def main() -> None:
    conn = get_connection()
    cur = conn.cursor()

    run_sql(cur, conn, sql_schema("01_clear_schema.sql"))
    run_sql(cur, conn, sql_schema("02_coworking.sql"))

    conn.commit()


if __name__ == "__main__":
    main()
