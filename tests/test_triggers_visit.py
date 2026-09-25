from tests.helpers import *

from coworking.cli.fill import *


def test_trg_on_insert_visit(conn, cur, faker: Faker, client_id: int, n_visits_to_insert: int) -> None:
    if n_visits_to_insert < 1:
        raise ValueError("`n_visits_to_insert` must be natural number")

    old_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='visits',
        where_col='client_id',
        where_value=client_id
    )

    assert len(old_row) == 1 and len(old_row[0]) == 1

    old_n_visits = old_row[0][0]

    n_inserted_visits = 0
    for _ in range(n_visits_to_insert):
        admin_id_list = get_id_list(cur, "administrator")
        agrs = get_client_agreement_dict(cur)
        agreement_id, end_time = None, datetime(1, 1, 1)
        if agrs and client_id in agrs.keys(): 
            agreement_id, end_time = choice(agrs[client_id])
        if not agreement_id:
            continue

        entrance_time = faker.date_time_between(
            start_date=end_time.date(),
            end_date=end_time
        ).replace(microsecond=0)
        exit_time = faker.date_time_between(
            start_date=entrance_time,
            end_date=end_time
        ).replace(microsecond=0)
        admin_id = choice(admin_id_list)

        insert_row(
            cur=cur,
            conn=conn,
            table_name='visit',
            columns=('activity_status', 'entrance_time', 'exit_time', 'client_id', 'admin_id', 'agreement_id'),
            values=(bool(randint(0, 1)), entrance_time, exit_time, client_id, admin_id, agreement_id)
        )
        n_inserted_visits += 1

    new_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='visits',
        where_col='client_id',
        where_value=client_id
    )

    assert len(new_row) == 1 and len(new_row[0]) == 1

    new_n_visits = new_row[0][0]

    assert new_n_visits - old_n_visits == n_inserted_visits


def test_trg_on_delete_visit(conn, cur, client_id: int) -> None:
    old_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='visits',
        where_col='client_id',
        where_value=client_id
    )
    assert len(old_row) == 1 and len(old_row[0]) == 1

    old_n_visits = old_row[0][0]

    rnd_visit_id = choice(select_rows(
        conn=conn,
        cur=cur,
        table_name='visit',
        columns='visit_id',
        where_col='client_id',
        where_value=client_id
    ))
    assert len(rnd_visit_id) == 1

    rnd_visit_id = rnd_visit_id[0]

    delete_rows(
        conn=conn,
        cur=cur,
        table_name='visit',
        col_name='visit_id',
        values=(rnd_visit_id,)
    )

    new_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='visits',
        where_col='client_id',
        where_value=client_id
    )

    assert len(new_row) == 1 and len(new_row[0]) == 1

    new_n_visits = new_row[0][0]

    assert old_n_visits - new_n_visits == 1


def main() -> None:
    conn = get_connection()
    cur = conn.cursor()
    faker = Faker("ru_RU")

    client_id_to_insert_visit = choice(get_id_list(cur, "client"))
    n_visits_to_insert = 10

    client_id_to_delete_visit = client_id_to_insert_visit

    test_trg_on_insert_visit(conn=conn, cur=cur, faker=faker, client_id=client_id_to_insert_visit, n_visits_to_insert=n_visits_to_insert)
    test_trg_on_delete_visit(conn=conn, cur=cur, client_id=client_id_to_delete_visit)


if __name__ == "__main__":
    main()
