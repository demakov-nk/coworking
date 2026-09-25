import json

from coworking.paths import STATIC_TABLES_FILE


def load_static_tables(path=STATIC_TABLES_FILE) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ERROR: file `{path}` not found")
        return dict()
    except json.JSONDecodeError:
        print(f"ERROR: JSON decode error while reading `{path}`")
        return dict()
