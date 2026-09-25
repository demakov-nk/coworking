from tests.helpers import *

from coworking.cli.fill import *

import pytest


def test_trg_on_insert_sub(conn, cur, faker: Faker, client_id: int, n_subs_to_insert: int) -> None:
    if n_subs_to_insert < 1:
        raise ValueError("`n_clients_to_insert` must be natural number")

    old_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='subs',
        where_col='client_id',
        where_value=client_id
    )

    assert len(old_row) == 1 and len(old_row[0]) == 1

    old_n_subs = old_row[0][0]

    for _ in range(n_subs_to_insert):
        admin_id_list = get_id_list(cur, "administrator")
        purchase_date = faker.date_this_century()
        cost = rnd_cost()
        start_date = faker.date_between(
            start_date=purchase_date, 
            end_date=timedelta(days=30)
        )
        end_date = faker.date_between(
            start_date=start_date + timedelta(days=7), 
            end_date=start_date + timedelta(days=37)
        )
        admin_id = choice(admin_id_list)

        insert_row(
            cur=cur,
            conn=conn,
            table_name='subscription',
            columns=('purchase_date', 'cost', 'start_date', 'end_date', 'admin_id', 'client_id'),
            values=(purchase_date, cost, start_date, end_date, admin_id, client_id)
        )

    new_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='subs',
        where_col='client_id',
        where_value=client_id
    )

    assert len(new_row) == 1 and len(new_row[0]) == 1

    new_n_subs = new_row[0][0]

    assert new_n_subs - old_n_subs == n_subs_to_insert


def test_trg_on_delete_sub(conn, cur, client_id: int) -> None:
    old_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='subs',
        where_col='client_id',
        where_value=client_id
    )
    assert len(old_row) == 1 and len(old_row[0]) == 1

    old_n_subs = old_row[0][0]

    rnd_sub_id = choice(select_rows(
        conn=conn,
        cur=cur,
        table_name='subscription',
        columns='subscription_id',
        where_col='client_id',
        where_value=client_id
    ))
    assert len(rnd_sub_id) == 1

    rnd_sub_id = rnd_sub_id[0]

    try:
        delete_rows(
            conn=conn,
            cur=cur,
            table_name='subscription',
            col_name='subscription_id',
            values=(rnd_sub_id,)
        )
    except RuntimeError as err:
        pytest.xfail(f"удаление невозможно из-за внешних ключей: {err}")

    new_row = select_rows(
        conn=conn,
        cur=cur,
        table_name='client_stats',
        columns='subs',
        where_col='client_id',
        where_value=client_id
    )

    assert len(new_row) == 1 and len(new_row[0]) == 1

    new_n_subs = new_row[0][0]

    assert old_n_subs - new_n_subs == 1


def main() -> None:
    conn = get_connection()
    cur = conn.cursor()
    faker = Faker("ru_RU")

    client_id_to_insert_sub = choice(get_id_list(cur, "client"))
    n_subs_to_insert = 10

    client_id_to_delete_sub = client_id_to_insert_sub

    test_trg_on_insert_sub(conn=conn, cur=cur, faker=faker, client_id=client_id_to_insert_sub, n_subs_to_insert=n_subs_to_insert)
    # test_trg_on_delete_sub(conn=conn, cur=cur, client_id=client_id_to_delete_sub)


if __name__ == "__main__":
    main()
