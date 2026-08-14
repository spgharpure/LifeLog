from tkinter import ttk

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Shreeya's Life Log", font=("Arial", 18)).pack(pady=10)
        ttk.Button(self, text="To-Do List", 
                   command=lambda: controller.show_frame("ToDoPage")).pack(pady=5)
        #ttk.Button(self, text="Habit Tracker", 
                   #command=lambda: controller.show_frame("HabitsPage")).pack(pady=5)

