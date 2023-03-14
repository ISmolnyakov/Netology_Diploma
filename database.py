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
                first_name varchar(50) NOT NULL,
                last_name varchar(25) NOT NULL,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50));"""
        )
        print("[DB Status] Table USERS was created.")


def creat_table_seen_users():
    with connection.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar(20) NOT NULL PRIMARY KEY,
            vk_link varchar(50));
            """
        )
    print("[DB Status] Table SEEN_USERS was created.")


def add_user_info(first_name, last_name, vk_id, vk_link):
    with connection.cursor() as cur:
        cur.execute(
            f"""
            INSERT INTO users (first_name, last_name, vk_id, vk_link)
            VALUES ('{first_name}', '{last_name}', '{vk_id}', '{vk_link}');
            """
        )


def add_seen_user_info(vk_id, vk_link):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (vk_id, vk_link) 
            VALUES ('{vk_id}', '{vk_link}');"""
        )


def get_user_id():
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id FROM users; """
        )
        return cursor.fetchall()


def get_seen_id():
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id FROM seen_users; """
        )
        return cursor.fetchall()


def drop_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ USERS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )
        print('[DB Status] Table USERS was deleted.')


def drop_seen_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ SEEN_USERS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS seen_users CASCADE;"""
        )
        print('[DB Status] Table SEEN_USERS was deleted.')


def creating_database():
    drop_users()
    drop_seen_users()
    create_table_users()
    creat_table_seen_users()
