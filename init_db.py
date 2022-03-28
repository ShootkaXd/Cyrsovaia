import sqlite3 as sql
from database import create_connection


def init_database(db_file: str):
    ctx = create_connection(db_file)
    cursor = ctx.cursor()

    create_users_table(cursor)
    ctx.commit()

    create_notes_table(cursor)
    ctx.commit()


def create_users_table(cursor: sql.Cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        ); 
    ''')


def create_notes_table(cursor: sql.Cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        note TEXT NOT NULL, 
        user_id INTEGER, 
        FOREIGN KEY (user_id) REFERENCES users (id)
            ON UPDATE CASCADE 
            ON DELETE CASCADE
    ); 
    ''')


if __name__ == '__main__':
    import sys
    init_database(sys.argv[1])

