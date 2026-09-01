import database.database as database

def add_goal(goal_text, term):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM goals")
    count = c.fetchone()[0]
    new_position = count

    c.execute("INSERT INTO goals (goat_text, term, position) VALUES (?, ?, ?)",
            (goal_text, term, new_position))

    conn.commit()
    conn.close()

def get_active_goals():
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM goals WHERE is_done = 0 ORDER BY position")
    rows = c.fetchall()

    conn.close()
    return rows

def get_archived_goals():
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM goals WHERE is_done = 1 ORDER BY goal_id DESC")
    rows = c.fetchall()

    conn.close()
    return rows

def set_goal_done(is_done, goal_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("UPDATE goals SET is_done = ? WHERE goal_id = ?",
              (is_done, goal_id))

    conn.commit()
    conn.close()

def delete_goal(goal_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM sub_goals WHERE goal_id = ?", (goal_id,))
    c.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))

    conn.commit()
    conn.close()

def add_sub_goal(goal_id, sub_goal_text):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("INSERT INTO sub_goals (goal_id, sub_goal_text) VALUES (?, ?)", (goal_id, sub_goal_text))

    conn.commit()
    conn.close()

def get_sub_goals(goal_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM sub_goals WHERE goal_id = ?", (goal_id,))
    rows = c.fetchall()

    conn.close()
    return rows

def set_sub_goal_done(sub_goal_id, is_done):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("UPDATE sub_goals SET is_done = ? WHERE sub_goal_id = ?", (is_done, sub_goal_id))

    conn.commit()
    conn.close()

def delete_sub_goal(sub_goal_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM sub_goals WHERE sub_goal_id = ?", (sub_goal_id,))

    conn.commit()
    conn.close()
