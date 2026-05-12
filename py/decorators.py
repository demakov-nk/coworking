def cache_ids(func):
    cache = dict()
    def wrapper(cur, table_name:str) -> list[int]:
        if table_name not in cache:
            cache[table_name] = func(cur, table_name)
        return cache[table_name]
    return wrapper


def cache_cs_dict(func):
    cache = dict()
    def wrapper(cur) -> dict[int, list[tuple]]:
        nonlocal cache
        if not cache:
            cache = func(cur)
        return cache
    return wrapper


def cache_ca_dict(func):
    cache = dict()
    def wrapper(cur) -> dict[int, list[tuple]]:
        nonlocal cache
        if not cache:
            cache = func(cur)
        return cache
    return wrapper


def cache_ces_dict(func):
    cache = dict()
    def wrapper(cur) -> dict[int, int]:
        nonlocal cache
        if not cache:
            cache = func(cur)
        return cache
    return wrapper
