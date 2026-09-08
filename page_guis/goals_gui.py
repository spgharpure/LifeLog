import tkinter as tk
from tkinter import ttk
import database.goals_db as goals_db

TERM_OPTIONS = ["No term", "Short term", "Long term"]

class GoalPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.goals = goals_db.get_active_goals()
        self.expanded_goal_ids = set()

        self.setup_styles()

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="<", width=3, style="Nav.TButton",
                              command=lambda: controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="Goals", font=("PT Mono", 20, "bold"))
        title.grid(row=0, column=1)

        add_frame = ttk.Frame(self)
        add_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.goal_entry = ttk.Entry(add_frame, font=("PT Mono", 12))
        self.goal_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
        self.goal_entry.bind("<Return>", self.add_goal)

        self.term_var = tk.StringVar(value=TERM_OPTIONS[0])
        term_dropdown = ttk.Combobox(add_frame, textvariable=self.term_var, values=TERM_OPTIONS,
                                     state="readonly", width=11, font=("PT Mono", 10))
        term_dropdown.pack(side="left", padx=(0, 8))

        ttk.Button(add_frame, text="Add", style="Nav.TButton", command=self.add_goal).pack(side="left")

        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.render_goals()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Nav.TButton", font=("PT Mono", 11))

    def add_goal(self, event=None):
        goal_text = self.goal_entry.get().strip()
        if not goal_text:
            return

        term = self.term_var.get()
        if term == "No term":
            term = None

        goals_db.add_goal(goal_text, term)
        self.goal_entry.delete(0, tk.END)
        self.term_var.set(TERM_OPTIONS[0])
        self.goals = goals_db.get_active_goals()
        self.render_goals()

    def toggle_done(self, goal_id, var):
        is_done = var.get()
        goals_db.set_goal_done(goal_id, is_done)
        self.goals = goals_db.get_active_goals()
        self.render_goals()

    def delete_goal(self, goal_id):
        goals_db.delete_goal(goal_id)
        self.expanded_goal_ids.discard(goal_id)
        self.goals = goals_db.get_active_goals()
        self.render_goals()

    def toggle_expanded(self, goal_id):
        if goal_id in self.expanded_goal_ids:
            self.expanded_goal_ids.remove(goal_id)
        else:
            self.expanded_goal_ids.add(goal_id)

        self.render_goals()

    def add_sub_goal(self, goal_id, entry_widget):
        text = entry_widget.get().strip()
        if not text:
            return
        goals_db.add_sub_goal(goal_id, text)
        self.render_goals()

    def toggle_sub_goal_done(self, sub_goal_id, var):
        goals_db.set_sub_goal_done(sub_goal_id, var.get())
        self.render_goals()

    def delete_sub_goal(self, sub_goal_id):
        goals_db.delete_sub_goal(sub_goal_id)
        self.render_goals()

    def render_goals(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for goal in self.goals:
            goal_id, goal_text, term, is_done, position = goal

            card = ttk.Frame(self.list_frame, padding=12, relief="solid", borderwidth=1)
            card.pack(fill="x", pady=5)

            top_row = ttk.Frame(card)
            top_row.pack(fill="x")

            done_var = tk.IntVar(value=is_done)
            done_chk = ttk.Checkbutton(top_row, variable=done_var, onvalue=1, offvalue=0,
                                       command=lambda gid=goal_id, v=done_var: self.toggle_done(gid, v))

            done_chk.pack(side="left")

            text_block = ttk.Frame(top_row)
            text_block.pack(side="left", fill="x", expand=True, padx=(6, 0))

            label_row = ttk.Frame(text_block)
            label_row.pack(fill="x", anchor="w")
            ttk.Label(label_row, text=goal_text, font=("PT Mono", 12, "bold")).pack(side="left")
            if term:
                ttk.Label(label_row, text=f"    [{term}]", font=("PT Mono", 9)).pack(side="left")
            
            delete_btn = ttk.Button(top_row, text="X", width=2, style="Nav.TButton", 
                                    command=lambda gid=goal_id: self.delete_goal(gid))
            delete_btn.pack(anchor="n", side="right")

            sub_goals = list(goals_db.get_sub_goals(goal_id))
            sub_done_count = sum(1 for sg in sub_goals if sg[3] == 1)
            is_expanded = goal_id in self.expanded_goal_ids
            arrow = "▾" if is_expanded else "▸"

            if sub_goals:
                toggle_text = f"{arrow} {sub_done_count} of {len(sub_goals)} sub-goals"
            else:
                toggle_text = f"{arrow} No sub-goals"

            expand_btn = ttk.Button(text_block, text=toggle_text, style="Nav.TButton",
                                    command=lambda gid=goal_id: self.toggle_expanded(gid))

            expand_btn.pack(anchor="w", pady=(4, 0))

            if is_expanded:
                sub_frame = ttk.Frame(text_block)
                sub_frame.pack(fill="x", padx=(10, 0), pady=(6, 0))

                for sub_goal in sub_goals:
                    sub_goal_id, _, sub_goal_text, sub_is_done = sub_goal

                    sub_row = ttk.Frame(sub_frame)
                    sub_row.pack(fill="x", pady=2)

                    sub_var = tk.IntVar(value=sub_is_done)
                    sub_chk = ttk.Checkbutton(sub_row, text=sub_goal_text, variable=sub_var, onvalue=1, offvalue=0,
                                              command=lambda sid=sub_goal_id, v=sub_var: self.toggle_sub_goal_done(sid, v))
                    sub_chk.pack(side="left")

                    sub_del_btn = ttk.Button(sub_row, text="X", width=2, style="Nav.TButton",
                                             command=lambda sid=sub_goal_id: self.delete_sub_goal(sid))

                    sub_del_btn.pack(side="right")

                new_sub_frame = ttk.Frame(sub_frame)
                new_sub_frame.pack(fill="x", pady=(4, 0))

                new_sub_entry = ttk.Entry(new_sub_frame, font=("PT Mono", 10))
                new_sub_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
                new_sub_entry.bind("<Return>", lambda e, gid=goal_id, ent=new_sub_entry: self.add_sub_goal(gid, ent))

                add_sub_btn = ttk.Button(new_sub_frame, text="+", width=2, style="Nav.TButton",
                                         command=lambda gid=goal_id, ent=new_sub_entry: self.add_sub_goal(gid, ent))
                add_sub_btn.pack(side="left")

    def refresh(self):
        self.goals = goals_db.get_active_goals()
        self.render_goals()






