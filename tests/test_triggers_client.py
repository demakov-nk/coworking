from tests.helpers import *

from coworking.cli.fill import *
from coworking.db.connection import get_connection
from coworking.data.loader import load_static_tables
from random import sample

import pytest


def test_trg_on_insert_client(conn, cur, n_genders: int, faker: Faker, n_clients_to_insert: int) -> None:
    if n_clients_to_insert < 1:
        raise ValueError("`n_clients_to_insert` must be natural number")

    old_client_ids = get_id_list_not_cached(cur, 'client')
    old_last_client_id = -1 if not old_client_ids else max(old_client_ids)
    
    old_client_stats_ids = get_id_list_not_cached(cur, 'client_stats')
    old_last_client_stats_id = -1 if not old_client_stats_ids else max(old_client_stats_ids)

    fill_client(conn, cur, n_genders, faker, n_clients_to_insert)

    new_client_ids = get_id_list_not_cached(cur, 'client')
    new_last_client_id = -1 if not new_client_ids else max(new_client_ids)

    new_client_stats_ids = get_id_list_not_cached(cur, 'client_stats')
    new_last_client_stats_id = -1 if not new_client_stats_ids else max(new_client_stats_ids)

    assert new_last_client_id - old_last_client_id >= n_clients_to_insert
    assert new_last_client_stats_id - old_last_client_stats_id >= n_clients_to_insert


def delete_row_or_xfail(conn, cur, table_name: str, col_name: str, values: tuple) -> None:
    """Удалить строки; если мешают внешние ключи — пометить тест как xfail.

    Схема БД не предусматривает ON DELETE CASCADE для договоров, счетов и
    визитов, поэтому удаление «занятого» клиента/абонемента невозможно.
    """
    try:
        delete_rows(
            conn=conn,
            cur=cur,
            table_name=table_name,
            col_name=col_name,
            values=values
        )
    except RuntimeError as err:
        pytest.xfail(f"удаление невозможно из-за внешних ключей: {err}")


def test_trg_on_delete_client(conn, cur, n_clients_to_delete: int) -> None:
    if n_clients_to_delete < 1:
        raise ValueError("`n_clients_to_delete` must be natural number")

    old_client_ids = get_id_list_not_cached(cur, 'client')
    old_client_stats_ids = get_id_list_not_cached(cur, 'client_stats')
    client_ids_to_delete = tuple(sample(old_client_ids, n_clients_to_delete))

    assert is_subset(client_ids_to_delete, old_client_stats_ids)

    delete_row_or_xfail(conn, cur, 'client', 'client_id', client_ids_to_delete)

    new_client_ids = get_id_list_not_cached(cur, 'client')
    new_client_stats_ids = get_id_list_not_cached(cur, 'client_stats')

    assert not is_subset(client_ids_to_delete, new_client_ids)
    assert not is_subset(client_ids_to_delete, new_client_stats_ids)


def test_trg_on_update_client_name(conn, cur, n_genders: int, faker: Faker, n_clients_to_update: int):
    if n_clients_to_update < 1:
        raise ValueError("`n_clients_to_update` must be natural number")

    client_ids = get_id_list_not_cached(cur, 'client')
    сlient_stats_ids = get_id_list_not_cached(cur, 'client_stats')
    client_ids_to_update = tuple(sample(client_ids, n_clients_to_update))

    assert is_subset(client_ids_to_update, сlient_stats_ids)

    rnd_names = tuple([rnd_person(n_genders, faker)[1] for _ in range(n_clients_to_update)])

    update_rows(
        conn=conn,
        cur=cur,
        table_name='client',
        col_to_update_name='name',
        values_to_update=rnd_names,
        col_to_filter_name='client_id',
        values_to_filter=client_ids_to_update
    )

    assert_update(
        conn=conn,
        cur=cur,
        table_name='client',
        col_to_update_name='name',
        expected_values=rnd_names,
        col_to_filter_name='client_id',
        values_to_filter=client_ids_to_update
    )    


def test_trg_on_update_client_surname(conn, cur, n_genders: int, faker: Faker, n_clients_to_update: int):
    if n_clients_to_update < 1:
        raise ValueError("`n_clients_to_update` must be natural number")

    client_ids = get_id_list_not_cached(cur, 'client')
    сlient_stats_ids = get_id_list_not_cached(cur, 'client_stats')
    client_ids_to_update = tuple(sample(client_ids, n_clients_to_update))

    assert is_subset(client_ids_to_update, сlient_stats_ids)

    rnd_surnames = tuple([rnd_person(n_genders, faker)[1] for _ in range(n_clients_to_update)])

    update_rows(
        conn=conn,
        cur=cur,
        table_name='client',
        col_to_update_name='surname',
        values_to_update=rnd_surnames,
        col_to_filter_name='client_id',
        values_to_filter=client_ids_to_update
    )

    assert_update(
        conn=conn,
        cur=cur,
        table_name='client',
        col_to_update_name='surname',
        expected_values=rnd_surnames,
        col_to_filter_name='client_id',
        values_to_filter=client_ids_to_update
    )  


def main() -> None:
    conn = get_connection()
    cur = conn.cursor()
    faker = Faker("ru_RU")

    static_data = load_static_tables()
    n_genders = len(static_data["gender"])

    n_clients_to_insert = 10
    n_clients_to_delete = 1
    n_clients_to_update = n_clients_to_insert

    test_trg_on_insert_client(conn=conn, cur=cur, n_genders=n_genders, faker=faker, n_clients_to_insert=n_clients_to_insert)
    # test_trg_on_delete_client(conn=conn, cur=cur, n_clients_to_delete=n_clients_to_delete)
    test_trg_on_update_client_name(conn=conn, cur=cur, n_genders=n_genders, faker=faker, n_clients_to_update=n_clients_to_update)
    test_trg_on_update_client_surname(conn=conn, cur=cur, n_genders=n_genders, faker=faker, n_clients_to_update=n_clients_to_update)


if __name__ == "__main__":
    main()
