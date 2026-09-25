from psycopg2 import sql
from psycopg2.extras import execute_values


def is_subset(a, b) -> bool:
    return set(a).issubset(set(b))


def delete_rows(conn, cur, table_name: str, col_name: str, values: tuple) -> None:
    if not values:
        return

    rows = [(v,) for v in values]

    try:
        execute_values(
            cur,
            f"""
            DELETE FROM {table_name} WHERE {col_name} IN (VALUES %s)
            """,
            rows,
            template="(%s)"
        )
    except Exception as err:
        conn.rollback()
        raise RuntimeError(f"ERROR (`{table_name}`): {err}")

    conn.commit()


def update_rows(conn, cur, table_name: str, 
                col_to_update_name: str, values_to_update: tuple,
                col_to_filter_name: str, values_to_filter: tuple) -> None:
    if len(values_to_update) != len(values_to_filter):
        raise ValueError(f"`values_to_update` and `values_to_filter` must have the same length ({len(values_to_update)} and {len(values_to_filter)} given)")

    if not values_to_update: return

    query = sql.SQL(
        "UPDATE {table} SET {set_col} = %s WHERE {filter_col} = %s"
    ).format(
        table=sql.Identifier(table_name),
        set_col=sql.Identifier(col_to_update_name),
        filter_col=sql.Identifier(col_to_filter_name),
    )

    pairs = list(zip(values_to_update, values_to_filter))

    try:
        cur.executemany(query, pairs)
    except Exception as err:
        conn.rollback()
        raise RuntimeError(f"ERROR (`{table_name}`): {err}")

    conn.commit()


def assert_update(conn, cur, table_name: str,
                  col_to_update_name: str, expected_values: tuple,
                  col_to_filter_name: str, values_to_filter: tuple) -> None:
    if len(expected_values) != len(values_to_filter):
        raise ValueError(f"`expected_values` and `values_to_filter` must have the same length ({len(expected_values)} and {len(values_to_filter)} given)")

    if not expected_values: return

    query = sql.SQL(
        "SELECT {col_to_update} FROM {table} WHERE {col_to_filter} = %s"
    ).format(
        col_to_update=sql.Identifier(col_to_update_name),
        table=sql.Identifier(table_name),
        col_to_filter=sql.Identifier(col_to_filter_name),
    )

    for expected, filter_value in zip(expected_values, values_to_filter):
        cur.execute(query, (filter_value,))
        rows = cur.fetchall()

        assert rows

        actual_values = {row[0] for row in rows}

        assert actual_values == {expected}
    

def select_rows(conn, cur, table_name: str, columns: tuple | list | str,
                where_col: str, where_value) -> list[tuple]:
    if not where_col:
        raise ValueError("`where_col` cannot be an empty string")

    if columns == "*":
        cols_sql = sql.SQL("*")
    elif isinstance(columns, str):
        cols_sql = sql.Identifier(columns)
    else:
        cols_sql = sql.SQL(", ").join(sql.Identifier(c) for c in columns)

    query = sql.SQL(
        "SELECT {cols} FROM {table} WHERE {col} = %s"
    ).format(
        cols=cols_sql,
        table=sql.Identifier(table_name),
        col=sql.Identifier(where_col),
    )

    cur.execute(query, (where_value,))
    return cur.fetchall()


def insert_row(
    conn, cur,
    table_name: str,
    columns: tuple | list,
    values: tuple,
) -> int:
    if not columns:
        raise ValueError("`columns` cannot be empty")

    if not values:
        raise ValueError("`values` cannot be empty")

    if len(columns) != len(values):
        raise ValueError(
            f"`columns` and `values` must have the same length "
            f"({len(columns)} and {len(values)} given)"
        )

    if isinstance(columns, str):
        columns = (columns,)

    cols_sql = sql.SQL(", ").join(sql.Identifier(c) for c in columns)

    placeholders = sql.SQL(", ").join(sql.Placeholder() * len(values))

    query = sql.SQL(
        "INSERT INTO {table} ({cols}) VALUES ({placeholders}) RETURNING *"
    ).format(
        table=sql.Identifier(table_name),
        cols=cols_sql,
        placeholders=placeholders,
    )

    try:
        cur.execute(query, values)
        row = cur.fetchone()
    except Exception as err:
        conn.rollback()
        raise RuntimeError(f"ERROR (`{table_name}`): {err}") from err

    conn.commit()
    return row

