from connection import get_connection


def run_sql(cur, conn, file_name:str):
    with open(file_name, "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";")
        for command in sql_commands:
            command = command.strip()
            if command:
                cur.execute(command)
        conn.commit()


if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()

    run_sql(cur, conn, "sql/clear_schema.sql")
    run_sql(cur, conn, "sql/coworking.sql")
        
    conn.commit()
