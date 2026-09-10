import database.database as database

def get_today_log(log_date):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM water_log WHERE log_date = ?", (log_date,))
    row = c.fetchone()

    conn.close()

    if row:
        return row
    return None

def ensure_today_log_exists(log_date):
    exists = get_today_log(log_date)

    conn = database.get_connection()
    c = conn.cursor()

    if not exists:  
        c.execute("INSERT INTO water_log (log_date) VALUES (?)", (log_date,))

    conn.commit()
    conn.close()


def adjust_ounces(amount, log_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT ounces FROM water_log WHERE log_id = ?", (log_id,))

    new_amount = max(0, c.fetchone()[0] + amount)

    c.execute("UPDATE water_log SET ounces = ? WHERE log_id = ?", (new_amount, log_id))

    conn.commit()
    conn.close()

def set_daily_goal(log_id, new_goal):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("UPDATE water_log SET daily_goal = ? WHERE log_id = ?", (new_goal, log_id))

    conn.commit()
    conn.close()