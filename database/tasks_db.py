import database.database as database

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

def get_all_tasks():
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM tasks ORDER BY position")
    rows = c.fetchall()

    conn.close()
    return rows

def delete_task(task_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))

    conn.commit()
    conn.close()

def update_positions(task_ids_in_order):
    conn = database.get_connection()
    c = conn.cursor()

    for new_position, task_id in enumerate(task_ids_in_order):
        c.execute("UPDATE tasks SET position = ? WHERE task_id = ?",
                  (new_position, task_id))

    conn.commit()
    conn.close()

def set_status(task_id, new_status):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("UPDATE tasks SET status = ? WHERE task_id = ?",
              (new_status, task_id))

    conn.commit()
    conn.close()

    
