import database.database as database

def set_mood(mood_date, mood_value):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT mood_id from moods WHERE mood_date = ?", (mood_date,))
    existing = c.fetchone()

    if existing:
        c.execute("UPDATE moods SET mood_value = ? WHERE mood_date = ?",
                  (mood_value, mood_date))
    else:
        c.execute("INSERT INTO moods (mood_date, mood_value) VALUES (?, ?)",
                  (mood_date, mood_value))

    conn.commit()
    conn.close()

def get_all_moods():
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM moods ORDER BY mood_date DESC")
    rows = c.fetchall()

    conn.close()
    return rows

def get_mood_for_date(mood_date):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT mood_value FROM moods WHERE mood_date = ?", (mood_date,))
    row = c.fetchone()

    conn.close()
    if row:
        return row[0]
    return None