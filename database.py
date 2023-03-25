import psycopg2
from config import *

connection = psycopg2.connect(
    user=user,
    password=password,
    database=db_name)

connection.autocommit = True


def create_table_users():
    with connection.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                full_name varchar(90) NOT NULL);"""
        )
        print("[DB Status] Table USERS was created.")


def creat_table_seen_users():
    with connection.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar(20) NOT NULL PRIMARY KEY);
            """
        )
    print("[DB Status] Table SEEN_USERS was created.")


def add_user_info(vk_id, full_name):
    with connection.cursor() as cur:
        cur.execute(
            f"""
            INSERT INTO users (vk_id, full_name)
            VALUES ('{vk_id}', '{full_name}');
            """
        )


def add_seen_user_info(vk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (vk_id) 
            VALUES ('{vk_id}');"""
        )


def get_user_data():
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id, full_name FROM users; """
        )
        return cursor.fetchall()


def get_seen_id():
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id FROM seen_users; """
        )
        return cursor.fetchall()


def creating_database():
    create_table_users()
    creat_table_seen_users()
