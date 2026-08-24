import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
import database.habits_db as habits_db

class HabitPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.habits = habits_db.get_all_habits()

        self.setup_styles()

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="<", width=3, style="Nav.TButton", 
                              command=lambda: controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="Habit Tracker", font=("PT Mono", 18, "bold"))
        title.grid(row=0, column=1)

        add_frame = ttk.Frame(self)
        add_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.habit_entry = ttk.Entry(add_frame, font=("PT Mono", 12))
        self.habit_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
        self.habit_entry.bind("<Return>", self.add_habit)

        self.category_entry = ttk.Entry(add_frame, font=("PT Mono", 12), width=14)
        self.category_entry.pack(side="left", padx=(0, 8), ipady=4)
        self.category_entry.bind("<Return>", self.add_habit)

        ttk.Button(add_frame, text="Add", style="Nav.TButton", command=self.add_habit).pack(side="left")

        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.render_habits()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Nav.TButton", font=("PT Mono", 11))
        style.configure("Day.TButton", font=("PT Mono", 10), width=3)
        style.configure("DayChecked.TButton", font=("PT Mono", 10), width=3,
                        background="#4CAF50", foreground="black")
        style.map("DayChecked.TButton", background=[("active", "#43A047")])

    def add_habit(self, event=None):
        habit_name = self.habit_entry.get().strip()
        category = self.category_entry.get().strip()
        if not habit_name:
            return

        habits_db.add_habit(habit_name, category)
        self.habit_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.habits = habits_db.get_all_habits()
        self.render_habits()

    def delete_habit(self, habit_id):
        habits_db.delete_habit(habit_id)
        self.habits = habits_db.get_all_habits()
        self.render_habits()

    def get_week_dates(self):
        today = date.today()
        days_since_sunday = (today.weekday() + 1) % 7
        sunday = today - timedelta(days=days_since_sunday)
        return [sunday + timedelta(days=i) for i in range(7)]

    def toggle_day(self, habit_id, checkin_date):
        habits_db.toggle_checkin(habit_id, checkin_date.strftime("%Y-%m-%d"))
        self.render_habits()

    def render_habits(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        week_dates = self.get_week_dates()
        today = date.today()
        day_letters = ["S", "M", "T", "W", "T", "F", "S"]

        for habit in self.habits:
            habit_id, habit_name, category, position = habit

            checked_dates = set(habits_db.get_checkins_for_habit(habit_id))
            streak = habits_db.calculate_streak(habit_id)
            checked_this_week = sum(1 for d in week_dates if d.strftime("%Y-%m-%d") in checked_dates)

            card = ttk.Frame(self.list_frame, padding=14, relief="solid", borderwidth=1)
            card.pack(fill="x", pady=6)

            top_row = ttk.Frame(card)
            top_row.pack(fill="x")
            top_row.columnconfigure(0, weight=1)

            name_block = ttk.Frame(top_row)
            name_block.grid(row=0, column=0, sticky="w")
            ttk.Label(name_block, text=habit_name, font=("PT Mono", 13, "bold")).pack(anchor="w")
            if category:
                ttk.Label(name_block, text=category, font=("PT Mono",10)).pack(anchor="w")

            streak_block = ttk.Frame(top_row)
            streak_block.grid(row=0, column=1, sticky="e")
            ttk.Label(streak_block, text=str(streak), font=("PT Mono", 16, "bold")).pack(anchor="e")
            ttk.Label(streak_block, text="day streak", font=("PT Mono", 9)).pack(anchor="e")

            del_btn = ttk.Button(top_row, text="X", width=2, style="Nav.TButton",
                                 command=lambda h=habit_id: self.delete_habit(h))
            del_btn.grid(row=0, column=2, sticky="e", padx=(8, 0))

            progress_label = ttk.Label(card, text=f"This week: {checked_this_week} / 7", font=("PT Mono", 9))
            progress_label.pack(anchor="w", pady=(8, 4))

            days_row = ttk.Frame(card)
            days_row.pack(fill="x", pady=(0, 4))

            for i, day_date in enumerate(week_dates):
                day_str = day_date.strftime("%Y-%m-%d")
                is_checked = day_str in checked_dates
                is_future = day_date > today

                button_style = "DayChecked.TButton" if is_checked else "Day.TButton"

                btn = ttk.Button(days_row, text=day_letters[i], style=button_style, 
                                 command=lambda h=habit_id, d=day_date: self.toggle_day(h, d))
                btn.pack(side="left", expand=True, fill="x", padx=2)

                if is_future:
                    btn.state(["disabled"])

    def refresh(self):
        self.habits = habits_db.get_all_habits()
        self.render_habits()



