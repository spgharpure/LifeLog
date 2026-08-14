import tkinter as tk
from tkinter import ttk

class ToDoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tasks = []