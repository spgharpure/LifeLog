import sqlite3

def get_connection():
    return sqlite3.connect("lifelog.db")

conn = get_connection()
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER NOT NULL PRIMARY KEY,
            task_name TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 0 CHECK (status IN (0, 1)),
            position INTEGER NOT NULL
            )""")

conn.commit()

