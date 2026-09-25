"""Подключение к PostgreSQL."""

import json
import os

from psycopg2 import connect

from coworking.paths import CONNECTION_CONFIG_FILE

CONFIG_ENV_VAR = "COWORKING_CONFIG"


def load_config(path=None) -> dict:
    """Прочитать параметры подключения из JSON-файла.

    Путь берётся из переменной окружения COWORKING_CONFIG, если она задана,
    иначе — из connection_config.json в корне проекта.
    """
    path = path or os.environ.get(CONFIG_ENV_VAR) or CONNECTION_CONFIG_FILE
    try:
        with open(path, "r", encoding="utf-8") as config:
            return json.load(config)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_connection():
    """Открыть соединение с БД, используя параметры из load_config()."""
    return connect(**load_config())
