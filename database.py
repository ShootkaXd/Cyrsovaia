import sqlite3 as sql


def create_connection(db_file):
    connection = None

    try:
        connection = sql.connect(db_file, timeout=10)
    except Exception as e:
        print(e)

    return connection


def get_all_notes(ctx: sql.Connection, user_id: int):
    cursor = ctx.cursor()

    cursor.execute("SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC", (user_id, ))

    return cursor.fetchall()


def post_note(ctx: sql.Connection, user_id: int, note: str):
    cursor = ctx.cursor()

    cursor.execute("INSERT INTO notes (note, user_id) VALUES (?, ?)", (note, user_id))

    ctx.commit()

    cursor.execute("SELECT * FROM notes WHERE note = ? and "
                   "user_id = ? ORDER BY id DESC LIMIT 1",
                   (note, user_id))

    return cursor.fetchone()


def delete_note(ctx: sql.Connection, id: int):
    cursor = ctx.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (id, ))


def auth_user(ctx: sql.Connection, name, password):
    cursor = ctx.cursor()

    cursor.execute("SELECT * FROM users WHERE name=? and password=?",
                   (name, password))
    user = cursor.fetchone()
    if user:
        return user[0]
    return None


def register(ctx: sql.Connection, name, password):
    cursor = ctx.cursor()
    cursor.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, password))
    ctx.commit()
    cursor.execute("SELECT * FROM users WHERE name=? and password=?",
                   (name, password))
    user = cursor.fetchone()
    if user:
        return user[0]
    return None

