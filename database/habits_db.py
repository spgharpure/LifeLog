import database.database as database
from datetime import date, timedelta

def add_habit(habit_name, category):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM habits")
    count = c.fetchone()[0]
    new_position = count

    c.execute("INSERT INTO habits (habit_name, category, position) VALUES (?, ?, ?)",
              (habit_name, category, new_position))

    conn.commit()
    conn.close()

def get_all_habits():
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM habits ORDER BY position")
    rows = c.fetchall()

    conn.close()
    return rows

def delete_habit(habit_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM habit_checkins WHERE habit_id = ?", (habit_id,))
    c.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))

    conn.commit()
    conn.close()

def update_positions(habit_ids_in_order):
    conn = database.get_connection()
    c = conn.cursor()

    for new_position, habit_id in enumerate(habit_ids_in_order):
        c.execute("UPDATE habits SET position = ? WHERE habit_id = ?",
                  (new_position, habit_id))

    conn.commit()
    conn.close()

def toggle_checkin(habit_id, checkin_date):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT checkin_id FROM habit_checkins WHERE habit_id = ? AND checkin_date = ?",
              (habit_id, checkin_date))

    existing = c.fetchone()

    if existing:
        c.execute("DELETE FROM habit_checkins WHERE checkin_id = ?", 
                  (existing[0], ))

    else:
        c.execute("INSERT INTO habit_checkins (habit_id, checkin_date) VALUES (?, ?)",
                  (habit_id, checkin_date))

    conn.commit()
    conn.close()

def get_checkins_for_habit(habit_id):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT checkin_date FROM habit_checkins WHERE habit_id = ?", (habit_id,))
    rows = c.fetchall()

    conn.close()
    return [row[0] for row in rows]

def set_status(habit_id, new_status):
    conn = database.get_connection()
    c = conn.cursor()

    c.execute("UPDATE habits SET status  = ? WHERE habit_id = ?",
              (new_status, habit_id))

    conn.commit()
    conn.close()

def calculate_streak(habit_id):
    checkin_dates = get_checkins_for_habit(habit_id)
    checkin_dates = set(checkin_dates)

    streak = 0
    current_day = date.today()

    while current_day.strftime("%Y-%m-%d") in checkin_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak