import database

def add_task(task_name):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM tasks")
    count = c.fetchone()[0]
    new_position = count

    c.execute("INSERT INTO tasks (task_name, position) VALUES (?, ?)",
              (task_name, new_position))

    conn.commit()
    conn.close()