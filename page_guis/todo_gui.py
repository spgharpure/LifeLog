import tkinter as tk
from tkinter import ttk
import database.database as database

class ToDoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tasks = []

        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="<", width=3, command=lambda: controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="To-Do List", font=("Arial", 18))
        title.grid(row=0, column=1)


        add_frame = ttk.Frame(self)
        add_frame.pack(fill="x", padx=10, pady=5)

        self.task_entry = ttk.Entry(add_frame)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.task_entry.bind("<Return>", self.add_task)

        ttk.Button(add_frame, text="Add", command=self.add_task).pack(side="left")

        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def add_task(self, event=None):
        task_text = self.task_entry.get().strip()
        if not task_text:
            return

        self.tasks.append({"text" : task_text, "done": tk.IntVar()})
        self.task_entry.delete(0, tk.END)
        self.render_tasks()

    def move_task(self, index, direction):
        new_index = index + direction
        if 0 <= new_index < len(self.tasks):
            self.tasks[index], self.tasks[new_index] = self.tasks[new_index], self.tasks[index]
            self.render_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.render_tasks()

    def render_tasks(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.tasks):
            row = ttk.Frame(self.list_frame)
            row.pack(fill="x", pady=2)

            up_btn = ttk.Button(row, text="↑", width=2, command=lambda i=i: self.move_task(i, -1))

            up_btn.pack(side="left")
            if i == 0:
                up_btn.state(["disabled"])

            down_btn = ttk.Button(row, text="↓", width=2,  command=lambda i=i: self.move_task(i, 1))

            down_btn.pack(side="left")
            if i == len(self.tasks) - 1:
                down_btn.state(["disabled"])

            chk = ttk.Checkbutton(row, text=task["text"], variable=task["done"])
            chk.pack(side="left", padx=5)

            del_btn = ttk.Button(row, text="X", width=2, command= lambda i=i: self.delete_task(i))
            del_btn.pack(side="right")

    def refresh(self):
        pass
        