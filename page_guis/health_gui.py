import tkinter as tk
from tkinter import ttk
from datetime import date
import database.water_db as water_db

class HealthPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.setup_styles()

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="X", width=3, style="Nav.TButton",
                              command=lambda: controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="Health", font=("PT Mono", 20, "bold"))
        title.grid(row=0, column=1)

        self.water_card = ttk.Frame(self, padding=14, relief="solid", borderwidth=1)
        self.water_card.pack(fill="x", padx=20, pady=(0, 10))

        for label in ["Sleep Log", "Exericise Log", "Supplements & Medicine"]:
            placeholder = ttk.Frame(self, padding=14, relief="solid", borderwidth=1)
            placeholder.pack(fill="x", padx=20, pady=(0, 10))
            ttk.Label(placeholder, text=label, font=("PT Mono", 12, "bold")).pack(anchor="w")

        self.render_water_card()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Nav.TButton", font=("PT Mono", 11))

    def render_water_card(self):
        for widget in self.water_card.winfo_children():
            widget.destroy()

        today_str = self.get_today_str()
        water_db.ensure_today_log_exists(today_str)
        log = water_db.get_today_log(today_str)
        log_id, log_date, ounces, daily_goal = log

        top_row = ttk.Frame(self.water_card)
        top_row.pack(fill="x")
        top_row.columnconfigure(0, weight=1)

        ttk.Label(top_row, text="Water Intake", font=("PT Mono", 13, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(top_row, text=f"{ounces} / {daily_goal} oz", font=("PT Mono", 11)).grid(row=0, column=1, sticky="e")

        progress = ttk.Progressbar(self.water_card, orient="horizontal", mode="determinate",
                                   maximum=daily_goal if daily_goal > 0 else 1, value=ounces)

        progress.pack(fill="x", pady=(8, 12))

        controls_row = ttk.Frame(self.water_card)
        controls_row.pack(fill="x")

        minus_btn = ttk.Button(controls_row, text="-", width=3, style="Nav.TButton",
                               command=lambda: self.adjust_water(log_id, -1))
        minus_btn.pack(side="left")

        self.amount_entry = ttk.Entry(controls_row, font=("PT Mono", 11), width=6)
        self.amount_entry.pack(side="left", padx=6)

        add_btn = ttk.Button(controls_row, text="+", width=3, style="Nav.TButton",
                             command=lambda: self.adjust_water(log_id, 1))
        add_btn.pack(side="left")

        goal_btn = ttk.Button(controls_row, text="Set as goal", style="Nav.TButton",
                             command=lambda: self.edit_goal(log_id))
        goal_btn.pack(side="right")

    def adjust_water(self, log_id, sign):
        text = self.amount_entry.get().strip()

        if not text:
            amount = 1
        else:
            try:
                amount = int(text)
            except ValueError:
                return

        water_db.adjust_ounces(amount*sign, log_id)
        self.render_water_card()

    def edit_goal(self, log_id):
        try:
            new_goal = int(self.amount_entry.get().strip())
        except ValueError:
            return
        water_db.set_daily_goal(log_id, new_goal)
        self.amount_entry.delete(0, tk.END)
        self.render_water_card()

    def get_today_str(self):
        return date.today().strftime("%Y-%m-%d")

    def refresh(self):
        self.render_water_card()

