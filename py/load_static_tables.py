import json


path = "static_tables.json"


def load_static_tables(path=path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ERROR: file `{path}` not found")
        return dict()
    except json.JSONDecodeError:
        print(f"ERROR: JSON decode error while reading `{path}`")
        return dict()
