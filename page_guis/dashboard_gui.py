from tkinter import ttk
from database import habits_db, tasks_db
from datetime import date

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)

        title_block = ttk.Frame(header)
        title_block.grid(row=0, column=0, sticky="w")

        ttk.Label(self, text="Shreeya's Life Log", font=("PT Mono", 22, "bold")).pack(anchor="w", padx=20)
        self.date_label = ttk.Label(title_block, text=self.get_today_string(), font=("PT Mono", 11))
        self.date_label.pack(anchor="w")

        stats = ttk.Frame(self)
        stats.pack(fill="x", padx=20, pady=10)

        tasks_block = ttk.Frame(stats)
        tasks_block.grid(row=0, column=0, sticky="w", padx=(0, 30))
        ttk.Label(tasks_block, text="Tasks today", font=("PT Mono", 11, "bold")).pack(anchor="w")
        self.tasks_today_label = ttk.Label(tasks_block, text="0 / 0", font=("PT Mono", 20))
        self.tasks_today_label.pack(anchor="w")

        streak_block = ttk.Frame(stats)
        streak_block.grid(row=0, column=2, sticky="w", padx=(0, 30))
        ttk.Label(streak_block, text="Habit streak", font=("PT Mono", 11, "bold")).pack(anchor="w")
        self.streak_label = ttk.Label(streak_block, text="0 days", font=("PT Mono", 20, "bold"))
        self.streak_label.pack(anchor="w")


        ttk.Label(self, text="Go to", font=("PT Mono", 11, "bold")).pack(anchor="w", padx=20, pady=(20, 5))

        nav_grid = ttk.Frame(self)
        nav_grid.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for col in range(3):
            nav_grid.columnconfigure(col, weight=1)

        pages = [
            ("📋", "To-Do List", "ToDoPage"),
            ("🌱", "Habit Tracker", "HabitPage"),
            ("😊", "Mood Tracker", "MoodPage"),
            ("✍🏼", "Journal", "JournalPage"),
            ("🎯", "Goals", "GoalPage"),
            ("💪", "Health Tracker", "HealthPage"),
            ("💰", "Finance Tracker", "FinancePage"),
            ("📅", "Calendar", "CalendarPage"),
            ("📝", "Notes", "NotePage")
        ]

        for i, (icon, label, page_name) in enumerate(pages):
            row = i // 3
            col = i % 3
            self.create_nav_card(nav_grid, row, col, icon, label, page_name)

        self.refresh()

    def create_nav_card(self, parent, row, col, icon, label, page_name):
        card = ttk.Frame(parent, padding=14, relief="solid", borderwidth=1)
        card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

        ttk.Label(card, text=icon, font=("PT Mono", 16)).pack(anchor="w")
        ttk.Label(card, text=label, font=("PT Mono", 12, "bold")).pack(anchor="w", pady=(6, 0))

        def go(event=None):
            if page_name in self.controller.frames:
                self.controller.show_frame(page_name)
            else:
                print(f"{page_name} hasn't been built yet")

        card.bind("<Button-1>", go)
        for child in card.winfo_children():
            child.bind("<Button-1>", go)

    def get_today_string(self):
        return date.today().strftime("%A, %B, %d")

    def get_tasks_today_text(self):
        tasks = tasks_db.get_all_tasks()
        total = len(tasks)
        done = sum(1 for task in tasks if task[2] == 1)
        return f"{done} / {total}"

    def get_best_streak(self):
        habits = habits_db.get_all_habits()
        if not habits:
            return 0
        streaks = [habits_db.calculate_streak(h[0]) for h in habits]
        return max(streaks)

    def refresh(self):
        self.date_label.config(text=self.get_today_string())
        self.tasks_today_label.config(text=self.get_tasks_today_text())
        self.streak_label.config(text=f"{self.get_best_streak()} days")

    

