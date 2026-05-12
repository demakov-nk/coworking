from connection import get_connection
from load_static_tables import load_static_tables
from decorators import cache_ids, cache_cs_dict, cache_ca_dict, cache_ces_dict

from psycopg2.extras import execute_values
from faker import Faker
from random import randint, uniform, choice
from datetime import timedelta, datetime
from time import perf_counter


def fill_table(conn, cur, table_name:str, cols:tuple, data:list[tuple]):
    if any([len(record) != len(cols) for record in data]):
        return
    
    start = perf_counter()

    try:
        execute_values(
            cur,
            f"""
            INSERT INTO {table_name} ({', '.join(cols)}) 
            VALUES %s 
            ON CONFLICT DO NOTHING
            """,
            data,
            template="(" + ','.join(["%s"] * len(cols)) + ")"
        )
    except Exception as err:
        print(f"ERROR (`{table_name}`): {err}")
        conn.rollback()

    conn.commit()
    return round(perf_counter() - start, 4)


def rnd_person(n_genders:int, faker:Faker) -> list:
    surname = name = ""
    birthday = faker.date_of_birth(minimum_age=16)
    gender = randint(1, n_genders)
    if gender == 1:
        surname = faker.last_name_male()
        name = faker.first_name_male()
    elif gender == 2:
        surname = faker.last_name_female()
        name = faker.first_name_female()
    else:
        surname = faker.last_name_nonbinary()
        name = faker.first_name_nonbinary()

    return [surname, name, birthday, gender]


def rnd_cost():
    return uniform(100, 5000)


@cache_ids
def get_id_list(cur, table_name:str) -> list[int]:
    id_name = ""
    if table_name.endswith("_type"):
        id_name = "type_id"
    elif table_name == "administrator":
        id_name = "admin_id"
    elif table_name == "open_space_structure":
        id_name = "addition_id"
    else:
        id_name = table_name + "_id"

    cur.execute(f"SELECT {id_name} FROM {table_name}")
    return [row[0] for row in cur.fetchall()]


@cache_cs_dict
def get_client_subscription_dict(cur) -> dict[int, list[tuple]]:
    cs_dict = dict()
    cur.execute(
        """
        SELECT client_id, subscription_id, start_date, end_date
        FROM subscription
        """
    )

    for client_id, subscription_id, start_date, end_date in cur.fetchall():
        if client_id not in cs_dict.keys():
            cs_dict[client_id] = [(subscription_id, start_date, end_date)]
        else:
            cs_dict[client_id].append((subscription_id, start_date, end_date))
    return cs_dict


@cache_ca_dict
def get_client_agreement_dict(cur) -> dict[int, list[tuple]]:
    ca_dict = dict()
    cur.execute(
        """
        SELECT client_id, agreement_id, end_time
        FROM agreement
        """
    )

    for client_id, agreement_id, end_time in cur.fetchall():
        if client_id not in ca_dict.keys():
            ca_dict[client_id] = [(agreement_id, end_time)]
        else:
            ca_dict[client_id].append((agreement_id, end_time))
    return ca_dict


@cache_ces_dict
def get_client_extra_service_dict(cur) -> dict[int, list[int]]:
    ces_dict = dict()
    cur.execute(
        """
        SELECT client_id, extra_service_id
        FROM extra_service
        """
    )

    for client_id, extra_service_id in cur.fetchall():
        if client_id not in ces_dict.keys():
            ces_dict[client_id] = [extra_service_id]
        else:
            ces_dict[client_id].append(extra_service_id)
    return ces_dict


def get_valid_subs(cur, client_id:int, agreement_date):
    subs = get_client_subscription_dict(cur)[client_id]
    return [sub for sub, s, e in subs if s <= agreement_date <= e]


def fill_static_tables(conn, cur, static:dict):
    for table in static.keys():
        data = [(x,) for x in static[table]]

        col = "type_name"
        if table == "gender": col = "gender"
        
        fill_table(conn, cur, table, (col,), data)


def fill_open_space(conn, cur, n:int):
    data = [
        (uniform(100, 350), randint(30, 150)) 
        for _ in range(n)
    ]
    return fill_table( 
        conn,
        cur,
        "open_space", 
        (
            "area", 
            "capacity"
        ), 
        data
    )


def fill_administrator(conn, cur, n_genders:int, faker:Faker, n:int):
    data = [
        tuple(rnd_person(n_genders, faker) + 
              [uniform(10_000, 150_000), faker.date_this_century()]) 
        for _ in range(n)
    ]
    return fill_table(
        conn,
        cur,
        "administrator", 
        (
            "surname", 
            "name", 
            "birthday", 
            "gender", 
            "salary", 
            "start_working_date"
        ),
        data
    )


def fill_room(conn, cur, n_types:int, n:int):
    data = [
        (randint(1, n_types), uniform(3, 150), randint(1, 100), bool(randint(0, 1)))
        for _ in range(n)
    ]
    return fill_table(
        conn,
        cur,
        "room",
        (
            "type_id",
            "area",
            "capacity",
            "is_busy"
        ),
        data
    )


def fill_open_space_structure(conn, cur, n_min:int, n_max:int):
    open_space_id_list = get_id_list(cur, "open_space")
    zone_type_id_list = get_id_list(cur, "open_space_zone_type")

    data = []
    for open_space in open_space_id_list:
        n_zones = randint(n_min, n_max)
        for _ in range(n_zones):
            data.append(
                (open_space, choice(zone_type_id_list))
            )
    return fill_table(
        conn,
        cur,
        "open_space_structure",
        (
            "open_space_id",
            "zone_type_id"
        ),
        data
    )


def fill_client(conn, cur, n_genders:int, faker:Faker, n:int):
    admin_id_list = get_id_list(cur, "administrator")

    data = [
        tuple(rnd_person(n_genders, faker) + 
              [faker.email(), faker.msisdn(), choice(admin_id_list)]) 
        for _ in range(n)
    ]
    return fill_table(
        conn,
        cur,
        "client",
        (
            "surname",
            "name",
            "birthday",
            "gender",
            "email",
            "phone",
            "admin_id"
        ),
        data
    )


def fill_subscription(conn, cur, faker:Faker, n_min:int, n_max:int):
    admin_id_list = get_id_list(cur, "administrator")
    client_id_list = get_id_list(cur, "client")

    data = []
    for client in client_id_list:
        n_subs = randint(n_min, n_max)
        for _ in range(n_subs):
            purchase_date = faker.date_this_century()
            start_date = faker.date_between(
                start_date=purchase_date, 
                end_date=timedelta(days=30)
            )
            end_date = faker.date_between(
                start_date=start_date + timedelta(days=7), 
                end_date=start_date + timedelta(days=37)
            )
            admin_id = choice(admin_id_list)
            data.append((purchase_date, rnd_cost(), start_date, end_date, admin_id, client))
    return fill_table(
        conn,
        cur,
        "subscription",
        (
            "purchase_date",
            "cost",
            "start_date",
            "end_date",
            "admin_id",
            "client_id"
        ),
        data
    )


def fill_extra_service(conn, cur, faker:Faker, n_min:int, n_max:int):
    type_id_list = get_id_list(cur, "extra_service_type")
    client_id_list = get_id_list(cur, "client")

    data = []
    for client in client_id_list:
        n_services = randint(n_min, n_max)
        for _ in range(n_services):
            data.append((faker.date_this_century(), rnd_cost(), choice(type_id_list), client))
    return fill_table(
        conn,
        cur,
        "extra_service",
        (
            "purchase_date",
            "cost",
            "type_id",
            "client_id"
        ),
        data
    )


def fill_agreement(conn, cur, faker:Faker, n_min:int, n_max:int):
    admin_id_list = get_id_list(cur, "administrator")
    client_id_list = get_id_list(cur, "client")
    room_id_list = get_id_list(cur, "room")
    open_space_id_list = get_id_list(cur, "open_space")

    either_room_open_space = lambda rnd: (choice(room_id_list), None) if rnd else (None, choice(open_space_id_list))

    data = []
    for client in client_id_list:
        n_agreements = randint(n_min, n_max)
        for _ in range(n_agreements):
            conclusion_date = faker.date_this_century()
            end_time = faker.date_time_between(
                start_date=conclusion_date, 
                end_date=datetime.combine(conclusion_date, datetime.max.time().replace(microsecond=0))
            ).replace(microsecond=0)
            admin_id = choice(admin_id_list)
            room_id, open_space_id = either_room_open_space(randint(0, 1))
            valid_subs = get_valid_subs(cur, client, conclusion_date)
            subscription_id = choice(valid_subs) if valid_subs and randint(0, 1) else None
            cost = None if subscription_id else rnd_cost()
            data.append((conclusion_date, end_time, cost, admin_id, client, room_id, open_space_id, subscription_id))
    return fill_table(
        conn,
        cur,
        "agreement",
        (
            "conclusion_date",
            "end_time",
            "cost",
            "admin_id",
            "client_id",
            "room_id",
            "open_space_id",
            "subscription_id"
        ),
        data
    )


def fill_bill(conn, cur, faker:Faker, n_min:int, n_max:int):
    client_id_list = get_id_list(cur, "client")
    admin_id_list = get_id_list(cur, "administrator")

    data = []
    for client in client_id_list:
        n_bills = randint(n_min, n_max)
        for _ in range(n_bills):
            agreement_id, subscription_id, extra_service_id = None, None, None
            rnd = randint(1, 3)
            if rnd == 1:
                agrs = get_client_agreement_dict(cur)
                if agrs and client in agrs.keys(): agreement_id = choice(agrs[client])[0]
            elif rnd == 2:
                subs = get_client_subscription_dict(cur)
                if subs and client in subs.keys(): subscription_id = choice(subs[client])[0]
            else:
                es = get_client_extra_service_dict(cur)
                if es and client in es.keys(): extra_service_id = choice(es[client])
            if agreement_id == subscription_id == extra_service_id == None:
                continue

            cost = rnd_cost()
            invoice_date = faker.date_this_century()
            closing_period = timedelta(days=randint(1, 10))
            closing_date = None if not randint(0, 1) else faker.date_time_between(
                start_date=invoice_date,
                end_date=invoice_date + closing_period
            ).replace(microsecond=0)
            admin_id = choice(admin_id_list)

            data.append((cost, invoice_date, closing_period, closing_date, client, admin_id, agreement_id, subscription_id, extra_service_id))
    return fill_table(
        conn,
        cur,
        "bill",
        (
            "cost",
            "invoice_date",
            "closing_period",
            "closing_date",
            "client_id",
            "admin_id",
            "agreement_id",
            "subscription_id",
            "extra_service_id"
        ),
        data
    )


def fill_visit(conn, cur, faker:Faker, n_min:int, n_max:int):
    client_id_list = get_id_list(cur, "client")
    admin_id_list = get_id_list(cur, "administrator")

    data = []
    for client in client_id_list:
        n_visits = randint(n_min, n_max)
        for _ in range(n_visits):
            agrs = get_client_agreement_dict(cur)
            agreement_id, end_time = None, datetime(1, 1, 1)
            if agrs and client in agrs.keys(): agreement_id, end_time = choice(agrs[client])
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

            data.append((bool(randint(0, 1)), entrance_time, exit_time, client, admin_id, agreement_id))
    return fill_table(
        conn,
        cur,
        "visit",
        (
            "activity_status",
            "entrance_time",
            "exit_time",
            "client_id",
            "admin_id",
            "agreement_id"
        ),
        data
    )


if __name__ == "__main__":
    # LEVEL 1
    GENDER               = 2
    EXTRA_SERVICE_TYPE   = 10
    ROOM_TYPE            = 5
    OPEN_SPACE_ZONE_TYPE = 10
    OPEN_SPACE           = 100

    # LEVEL 2
    OPEN_SPACE           = 100
    ADMINISTRATOR        = 150
    ROOM                 = 500
    OPEN_SPACE_STRUCTURE = (2, 5)

    # LEVEL 3
    CLIENT = 3500

    # LEVEL 4
    SUBSCRIPTION  = (1, 5)
    EXTRA_SERVICE = (0, 5)

    # LEVEL 5
    AGREEMENT = (1, 20)

    # LEVEL 6
    BILL  = (50, 70)
    VISIT = (1, 15)

    conn = get_connection()
    cur = conn.cursor()
    faker = Faker("ru_RU")

    static_data = load_static_tables()
    n_genders = len(static_data["gender"])

    print(f"Static tables: {fill_static_tables(conn, cur, static_data)} sec")
    print(f"Open_space: {fill_open_space(conn, cur, OPEN_SPACE)} sec")
    print(f"Administrator: {fill_administrator(conn, cur, n_genders, faker, ADMINISTRATOR)} sec")
    print(f"Room: {fill_room(conn, cur, ROOM_TYPE, ROOM)} sec")
    print(f"Open_space_structure: {fill_open_space_structure(conn, cur, *OPEN_SPACE_STRUCTURE)} sec")
    print(f"Client: {fill_client(conn, cur, n_genders, faker, CLIENT)} sec")
    print(f"Subscription: {fill_subscription(conn, cur, faker, *SUBSCRIPTION)} sec")
    print(f"Extra_service: {fill_extra_service(conn, cur, faker, *EXTRA_SERVICE)} sec")
    print(f"Agreement: {fill_agreement(conn, cur, faker, *AGREEMENT)} sec")
    print(f"Bill: {fill_bill(conn, cur, faker, *BILL)} sec")
    print(f"Visit: {fill_visit(conn, cur, faker, *VISIT)} sec")
