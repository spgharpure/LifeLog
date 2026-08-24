import tkinter as tk
from tkinter import ttk
from datetime import date
import database.moods_db as moods_db

MOOD_OPTIONS = ["Awful", "Bad", "Okay", "Good", "Great"]

MOOD_COLORS = {"Awful": "#E24B4A", "Bad": "#EF9F27", "Okay": "#B4B2A9", "Good": "#97C459", "Great": "#1D9E75"}

class MoodPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.setup_styles()

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="<", width=3, style="Nav.TButton",
                              command=lambda: controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="Mood Tracker", font=("PT Mono", 20, "bold"))
        title.grid(row=0, column=1)

        self.today_card = ttk.Frame(self, padding=14, relief="solid", borderwidth=1)
        self.today_card.pack(fill="x", padx=20, pady=(0, 15))

        ttk.Label(self, text="History", font=("PT Mono", 11)).pack(anchor="w", padx=20, pady=(0, 5))

        self.history_frame = ttk.Frame(self)
        self.history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.render_today_card()
        self.render_history()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Nav.TButton", font=("PT Mono", 11))
        for mood in MOOD_OPTIONS:
            style.configure(f"{mood}.TButton", font=("PT Mono", 10))
        style.configure("Selected.TButton",  font=("PT Mono", 10, "bold"), relief="solid", borderwidth=2)

    def get_today_string(self):
        return date.today().strftime("%A, %B, %d")

    def select_mood(self, mood_value):
        today_str = date.today().strftime("%Y-%m-%d")
        moods_db.set_mood(today_str, mood_value)
        self.render_today_card()
        self.render_history()

    def render_today_card(self):
        for widget in self.today_card.winfo_children():
            widget.destroy()

        ttk.Label(self.today_card, text="Today", font=("PT Mono", 11)).pack(anchor="w")
        ttk.Label(self.today_card, text=self.get_today_string(), font=("PT Mono", 13, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Label(self.today_card, text="How are you feeling today?", font=("PT Mono", 11)).pack(anchor="w", pady=(0, 8))

        today_str = date.today().strftime("%Y-%m-%d")
        current_mood = moods_db.get_mood_for_date(today_str)

        buttons_row = ttk.Frame(self.today_card)
        buttons_row.pack(fill="x")

        for mood in MOOD_OPTIONS:
            is_selected = (mood == current_mood)
            style_name = "Selected.TButton" if is_selected else f"{mood}.TButton"

            btn_frame = ttk.Frame(buttons_row)
            btn_frame.pack(side="left", expand=True, fill="x", padx=3)

            dot = tk.Canvas(btn_frame, width=16, height=16, highlightthickness=0, bg="#dcdad2")
            dot.create_oval(2, 2, 14, 14, fill=MOOD_COLORS[mood], outline="")
            dot.pack()

            btn = ttk.Button(btn_frame, text=mood, style=style_name,
                             command=lambda m=mood: self.select_mood(m))
            btn.pack(fill="x", pady=(4, 0))

    def render_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        moods = moods_db.get_all_moods()
        today_str = date.today().strftime("%Y-%m-%d")

        for mood_id, mood_date, mood_value in moods:
            if mood_date == today_str:
                continue

            row = ttk.Frame(self.history_frame, padding=10, relief="solid", borderwidth=1)
            row.pack(fill="x", pady=3)
            row.columnconfigure(0, weight=1)

            display_date = date.fromisoformat(mood_date).strftime("%A, %B, %d")
            ttk.Label(row, text=display_date, font=("PT Mono", 11)).grid(row=0, column=0, sticky="w")

            right_block = ttk.Frame(row)
            right_block.grid(row=0, column=1, sticky="e")

            ttk.Label(right_block, text=mood_value, font=("PT Mono", 10)).pack(side="left", padx=(0, 6))

            dot = tk.Canvas(right_block, width=14, height=14, highlightthickness=0, bg="#dcdad2")
            dot.create_oval(1, 1, 13, 13, fill=MOOD_COLORS[mood_value], outline="")
            dot.pack(side="left")

    def refresh(self):
        self.render_history()
        self.render_today_card()

        



