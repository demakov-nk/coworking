from connection import get_connection
from argparse import ArgumentParser
from tabulate import tabulate


def count_records(cur, table_name:str) -> int:
    cur.execute(f"""
        SELECT count(*)
        FROM {table_name}
    """)
    return cur.fetchone()[0]


def tables_list(cur) -> list[str]:
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    return [x[0] for x in cur.fetchall()]


def view_table(cur, table_name:str, rows:int) -> int:
    cur.execute(f"SELECT * FROM {table_name}")

    data = cur.fetchall()
    header = [col.name for col in cur.description]
    n_records = len(data)
    title = table_name + f" ({n_records} records)"
    data = data[:rows]

    table = tabulate(data, headers=header, tablefmt='pretty')
    table_width = len(table.split('\n')[0])
    print(f"\n{title:^{table_width}}")
    print(table)

    return n_records



if __name__ == "__main__":
    parser = ArgumentParser(description="Просмотр содержимого таблиц")
    parser.add_argument("--name", help="Имя таблицы")
    parser.add_argument("--rows", help="Количество строк из начала таблицы", type=int, default=10)

    args = parser.parse_args()
    conn = get_connection()
    cur = conn.cursor()

    if args.name:
        view_table(cur, args.name, args.rows)
    else:
        names = tables_list(cur)
        total_records = 0
        for table_name in names:
            total_records += view_table(cur, table_name, args.rows)

        print(f"\nTOTAL RECORDS: {total_records}")



