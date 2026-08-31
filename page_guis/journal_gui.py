import tkinter as tk
from tkinter import ttk
from datetime import date
import database.journal_db as journal_db

class JournalPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entries = journal_db.get_all_entries()
        self.current_entry_id = None

        self.setup_styles()

        self.grid_view = ttk.Frame(self)
        self.write_view = ttk.Frame(self)

        self.build_grid_view()
        self.build_write_view()

        self.show_grid_view()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Nav.TButton", font=("PT Mono", 11))

    def show_grid_view(self):
        self.write_view.pack_forget()
        self.grid_view.pack(fill="both", expand=True)
        self.entries = journal_db.get_all_entries()
        self.render_grid()

    def show_write_view(self, entry_id=None):
        self.grid_view.pack_forget()
        self.write_view.pack(fill="both", expand=True)
        self.current_entry_id = entry_id

        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

        if entry_id is not None:
            entry = next(e for e in self.entries if e[0] == entry_id)
            _, entry_date, title, content = entry
            self.write_date_label.config(text=self.format_date(entry_date))
            if title:
                self.title_entry.insert(0, title)
            if content:
                self.content_text.insert("1.0", content)
        else:
            self.write_date_label.config(text=self.format_date(date.today().strftime("%Y-%m-%d")))

    def format_date(self, date_str):
        return date.fromisoformat(date_str).strftime("%A, %B %d")

    def build_grid_view(self):
        header = ttk.Frame(self.grid_view)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        back_btn = ttk.Button(header, text="<", width=3, style="Nav.TButton",
                              command=lambda: self.controller.show_frame("DashboardPage"))
        back_btn.grid(row=0, column=0, sticky="w")

        title = ttk.Label(header, text="Journal", font=("PT Mono", 20, "bold"))
        title.grid(row=0, column=1)

        add_btn = ttk.Button(header, text="+", width=3, style="Nav.TButton", 
                             command=lambda: self.show_write_view(entry_id=None))
        add_btn.grid(row=0, column=2, sticky="e")

        self.grid_container = ttk.Frame(self.grid_view)
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.grid_container.columnconfigure(0, weight=1)
        self.grid_container.columnconfigure(1, weight=1)

    def render_grid(self):
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        for i, entry in enumerate(self.entries):
            entry_id, entry_date, title, content = entry
            row = i // 2
            col = i % 2

            preview = content.strip().replace("\n", " ") if content else "(no content)"
            if len(preview) > 90:
                preview = preview[:90] + "..."

            display_title = title if title else "Untitled"
            display_date = date.fromisoformat(entry_date).strftime("%b %d")

            card_text = f"{display_date}\n{display_title}\n{preview}"

            btn = tk.Button(self.grid_container, text=card_text, wraplength=220, justify="left", anchor="nw",
                            font=("PT Mono", 9), height=6, command=lambda eid=entry_id: self.show_write_view(entry_id=eid))
            btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

    def build_write_view(self):
        header = ttk.Frame(self.write_view)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)

        close_btn = ttk.Button(header, text="X", width=3, style="Nav.TButton",
                               command=self.close_without_saving)
        close_btn.grid(row=0, column=0, sticky="w")

        self.write_date_label = ttk.Label(header, text="", font=("PT Mono", 11))
        self.write_date_label.grid(row=0, column=1)

        save_btn = ttk.Button(header, text="Save", style="Nav.TButton",
                              command=self.save_entry)
        save_btn.grid(row=0, column=2, sticky="e")

        delete_btn = ttk.Button(header, text="Delete", style="Nav.TButton",
                                command=self.delete_entry)
        delete_btn.grid(row=0, column=3, sticky="e")

        self.title_entry = ttk.Entry(self.write_view, font=("PT Mono", 14))
        self.title_entry.pack(fill="x",  padx=20, pady=(0,10), ipady=4)

        self.content_text = tk.Text(self.write_view, font=("PT Mono", 11), wrap="word")
        self.content_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def save_entry(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not title and not content:
            return

        if self.current_entry_id is None:
            entry_date = date.today().strftime("%Y-%m-%d")
            journal_db.add_entry(entry_date, title, content)
        else:
            journal_db.update_entry(self.current_entry_id, title, content)

        self.show_grid_view()

    def close_without_saving(self):
        self.show_grid_view()

    def delete_entry(self):
        if self.current_entry_id is not None:
            journal_db.delete_entry(self.current_entry_id)
            self.show_grid_view()

    def refresh(self):
        self.entries = journal_db.get_all_entries()

        




