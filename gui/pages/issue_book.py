""" gui > pages > issue_book.py """
import tkinter as tk
from tkinter import ttk, messagebox
from database import member_db, book_db, transaction_db
from datetime import date


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
        self.create_table()
        self.load_issued_books()

        form_frame = ttk.Frame(self.content)
        form_frame.pack(pady=10, fill=tk.X)

        ttk.Label(form_frame, text="Member:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.member_combo = ttk.Combobox(form_frame, state="readonly")
        self.member_combo.grid(row=1, column=0, padx=5, pady=5)
        self.load_members()

        ttk.Label(form_frame, text="Book ID:").grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.book_combo = ttk.Combobox(form_frame, state="readonly")
        self.book_combo.grid(row=1, column=1, padx=5, pady=5)
        self.load_books()

        ttk.Label(form_frame, text="Issue Date:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.issue_date_entry = ttk.Entry(form_frame)
        self.issue_date_entry.insert(0, date.today().isoformat())
        self.issue_date_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(form_frame, text="Return Date:").grid(
            row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.return_date_entry = ttk.Entry(form_frame)
        self.return_date_entry.insert(0, date.today().isoformat())
        self.return_date_entry.grid(row=1, column=3, padx=5, pady=5)

        issue_button = ttk.Button(
            form_frame, text="Issue Book", command=self.submit_issue)
        issue_button.grid(row=2, column=4, pady=10)

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

    def submit_issue(self):
        try:
            member_label = self.member_combo.get()
            book_label = self.book_combo.get()

            if not member_label or not book_label:
                messagebox.showwarning(
                    "Validation Error", "Please select both member and book.")
                return

            member_id = self.member_map[member_label]
            book_id = self.book_map[book_label]
            issue_date = self.issue_date_entry.get()
            return_date = self.return_date_entry.get()

            if not issue_date or not return_date:
                messagebox.showwarning(
                    "Validation Error",
                    "Please enter both issue and return dates.")
                return

            transaction_db.issue_book(
                book_id, member_id, issue_date, return_date)
            messagebox.showinfo("Success", "Book issued successfully.")
            self.load_issued_books()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {e}")

    def create_table(self):
        columns = ("ID", "Book Title", "Member Name", "Issue Date", "Return Date", "Actual Return Date", "Fine")
        table_frame = ttk.Frame(self.content)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.issue_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.issue_table.heading(col, text=col)
            self.issue_table.column(col, width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.issue_table.yview)
        self.issue_table.configure(yscrollcommand=scrollbar.set)

        self.issue_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_issued_books(self):
        try:
            records = transaction_db.get_issue_book_history()
            self.issue_table.delete(*self.issue_table.get_children())
            for row in records:
                self.issue_table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load issued books: {e}")
