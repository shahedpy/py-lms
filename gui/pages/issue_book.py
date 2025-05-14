""" gui > pages > issue_book.py """
import tkinter as tk
from tkinter import ttk, messagebox
from database import member_db, book_db
from datetime import date, timedelta


class IssueBookPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self.content, text="📖 Issue Book", font=("Arial", 16, "bold")
        ).pack(pady=10)

        form_frame = ttk.Frame(self.content)
        form_frame.pack(pady=10, fill=tk.X)

        ttk.Label(form_frame, text="Member:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.member_combo = ttk.Combobox(form_frame, state="readonly")
        self.member_combo.grid(row=1, column=0, padx=5, pady=5)
        self.load_members()

        ttk.Label(form_frame, text="Book ID:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_combo = ttk.Combobox(form_frame, state="readonly")
        self.book_combo.grid(row=3, column=0, padx=5, pady=5)
        self.load_books()

        ttk.Label(form_frame, text="Issue Date:").grid(
            row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.issue_date_entry = ttk.Entry(form_frame)
        self.issue_date_entry.insert(0, date.today().isoformat())
        self.issue_date_entry.grid(row=5, column=0, padx=5, pady=5)

    def load_members(self):
        try:
            members = member_db.get_members()
            self.member_map = {f"{name} (ID: {id})": id for id, name, *_ in members} # noqa
            self.member_combo["values"] = list(self.member_map.keys())
            self.member_combo.current(0)
            if members:
                self.member_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")

    def load_books(self):
        try:
            books = book_db.get_books()
            self.book_map = {f"{title} (ID: {id})": id for id, title, *_ in books} # noqa
            self.book_combo["values"] = list(self.book_map.keys())
            self.book_combo.current(0)
            if books:
                self.book_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")
