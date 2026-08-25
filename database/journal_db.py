import database.database as database

def add_entry(entry_date, title, content):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("INSERT INTO journal_entries (entry_date, title, content) VALUES (? ,?, ?)",
              (entry_date, title, content))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM journal_entries ORDER BY entry_id DESC")
    rows = c.fetchall()

    conn.close()
    return rows

def update_entry(entry_id, title, content):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("UPDATE journal_entries SET title = ?, content = ? WHERE entry_id = ?",
              (title, content, entry_id))

    conn.commit()
    conn.close()

def delete_entry(entry_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM journal_entries WHERE entry_id = ?", (entry_id,))

    conn.commit()
    conn.close()