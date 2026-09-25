"""Применение SQL-файлов со схемой."""

from pathlib import Path


def run_sql(cur, conn, file_name: str | Path) -> None:
    """Выполнить SQL-инструкции из файла (инструкции разделены символом «;»)."""
    with open(file_name, "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";")
        for command in sql_commands:
            command = command.strip()
            if command:
                cur.execute(command)
        conn.commit()
