import psycopg2
from config import *

connection = psycopg2.connect(
    user=user,
    password=password,
    database=db_name)

connection.autocommit = True


def creat_table_seen_users():
    with connection.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar(20) NOT NULL PRIMARY KEY);
            """
        )
    print("[DB Status] Table SEEN_USERS was created.")


def add_seen_user_info(vk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (vk_id) 
            VALUES ('{vk_id}');"""
        )


def check_seen_id(id_num):
    with connection.cursor() as cur:
        cur.execute(
            """SELECT vk_id FROM seen_users WHERE vk_id=%s; """, (id_num, )
        )
        return cur.fetchone()


def creating_database():
    creat_table_seen_users()
