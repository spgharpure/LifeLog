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

c.execute("""CREATE TABLE IF NOT EXISTS habits (
            habit_id INTEGER NOT NULL PRIMARY KEY,
            habit_name TEXT NOT NULL,
            category TEXT,
            position INTEGER NOT NULL
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS habit_checkins (
            checkin_id INTEGER NOT NULL PRIMARY KEY,
            habit_id INTEGER NOT NULL,
            checkin_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (habit_id)
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS moods (
            mood_id INTEGER NOT NULL PRIMARY KEY,
            mood_date TEXT NOT NULL UNIQUE,
            mood_value TEXT NOT NULL)""")

conn.commit()

