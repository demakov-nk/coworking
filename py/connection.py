from psycopg2 import connect, errors
import json


config_name = "connection_config.json"


def load_config(path=config_name):
    try:
        with open(path, "r") as config:
            return json.load(config)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_connection():
    return connect(**load_config())
