import tkinter as tk
from tkinter import ttk
from dashboard_gui import DashboardPage
from todo_gui import ToDoPage

class LifeLogApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LifeLog")
        self.geometry("900x600")


        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for PageClass in (DashboardPage, ToDoPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DashboardPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = LifeLogApplication()
    app.mainloop()

