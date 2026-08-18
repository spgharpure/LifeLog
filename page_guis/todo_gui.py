import tkinter as tk
from tkinter import ttk
import database.database as database
import database.tasks_db as tasks_db

class ToDoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tasks = tasks_db.get_all_tasks()
        self.check_vars = []

        self.setup_styles()

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(20,10), padx=20)
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="<", width=3, command=lambda: controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="To-Do List", font=("PT Mono", 18, "bold"))
        title.grid(row=0, column=1)


        add_frame = ttk.Frame(self)
        add_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.task_entry = ttk.Entry(add_frame,font=("PT Mono", 12))
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
        self.task_entry.bind("<Return>", self.add_task)

        ttk.Button(add_frame, text="Add", style="Nav.TButton", command=self.add_task).pack(side="left")

        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.render_tasks()

    def add_task(self, event=None):
        task_text = self.task_entry.get().strip()
        if not task_text:
            return

        tasks_db.add_task(task_text)
        self.task_entry.delete(0, tk.END)
        self.tasks = tasks_db.get_all_tasks()
        self.render_tasks()

    def move_task(self, index, direction):
        new_index = index + direction
        if 0 <= new_index < len(self.tasks):
            self.tasks[index], self.tasks[new_index] = self.tasks[new_index], self.tasks[index]
            task_ids_in_order = [tasks[0] for task in self.tasks]
            tasks_db.update_positions(task_ids_in_order)
            self.tasks = tasks_db.get_all_tasks()
            self.render_tasks()

    def delete_task(self, index):
        task_id = self.tasks[index][0]
        tasks_db.delete_task(task_id)
        self.tasks = tasks_db.get_all_tasks()
        self.render_tasks()

    def render_tasks(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.check_vars = []

        for i, task in enumerate(self.tasks):
            task_id, task_name, status, position = task

            row = ttk.Frame(self.list_frame)
            row.pack(fill="x", pady=2)

            up_btn = ttk.Button(row, text="↑", width=2, style="Nav.TButton", command=lambda i=i: self.move_task(i, -1))

            up_btn.pack(side="left")
            if i == 0:
                up_btn.state(["disabled"])

            down_btn = ttk.Button(row, text="↓", width=2, style="Nav.TButton", command=lambda i=i: self.move_task(i, 1))

            down_btn.pack(side="left")
            if i == len(self.tasks) - 1:
                down_btn.state(["disabled"])

            var = tk.IntVar(value=status)
            self.check_vars.append(var)
            chk = ttk.Checkbutton(row, text=task_name, variable=var, onvalue=1, offvalue=0, style="Task.TCheckbutton",
                                  command=lambda task_id=task_id, var=var: self.toggle_status(task_id, var))
            chk.pack(side="left", padx=5)

            del_btn = ttk.Button(row, text="X", width=2, style="Nav.TButton", command= lambda i=i: self.delete_task(i))
            del_btn.pack(side="right")

    def refresh(self):
        self.tasks = tasks_db.get_all_tasks()
        self.render_tasks

    def toggle_status(self, task_id, var):
        new_status = var.get()
        tasks_db.set_status(task_id, new_status)
        self.tasks = tasks_db.get_all_tasks()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Nav.TButton", font=("PT Mono", 11))
        style.configure("Task.TCheckbutton", font=("PT Mono", 12))
        style.configure("Task.TFrame", relief="solid", borderwidth=1)