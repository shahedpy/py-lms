""" gui > pages > return_book.py """
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import transaction_db


class ReturnBookPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_unreturned_books()

    def create_widgets(self):
        ttk.Label(
            self.content,
            text="📘 Return Book",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        columns = (
            "ID", "Book Title", "Member Name", "Issue Date", "Return Date")
        self.table = ttk.Treeview(
            self.content, columns=columns, show="headings")
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120)
        self.table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_row_select)

        form = ttk.Frame(self.content)
        form.pack(pady=10)

        ttk.Label(
            form, text="Transaction ID:").grid(row=0, column=0, padx=5, pady=5)
        self.transaction_id_entry = ttk.Entry(form)
        self.transaction_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(
            form, text="Return Date:").grid(row=0, column=2, padx=5, pady=5)
        self.return_date_entry = ttk.Entry(form)
        self.return_date_entry.insert(0, date.today().isoformat())
        self.return_date_entry.grid(row=0, column=3, padx=5, pady=5)

        return_btn = ttk.Button(
            form, text="Return Book", command=self.return_book)
        return_btn.grid(row=0, column=4, padx=10, pady=5)

    def load_unreturned_books(self):
        try:
            records = transaction_db.get_issue_book_history()
            self.table.delete(*self.table.get_children())
            for row in records:
                transaction_id, book, member, issue_date, return_date, actual_return_date, _ = row # noqa
                if actual_return_date is None:
                    self.table.insert(
                        "", tk.END,
                        values=(
                            transaction_id, book, member,
                            issue_date, return_date)
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def on_row_select(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item_values = self.table.item(selected_item[0], 'values')
            transaction_id = item_values[0]
            self.transaction_id_entry.delete(0, tk.END)
            self.transaction_id_entry.insert(0, transaction_id)

    def return_book(self):
        try:
            transaction_id = self.transaction_id_entry.get().strip()
            actual_return_date = self.return_date_entry.get().strip()

            if not transaction_id or not actual_return_date:
                messagebox.showwarning(
                    "Input Error",
                    "Please enter both transaction ID and return date.")
                return

            transaction_db.return_book(int(transaction_id), actual_return_date)
            messagebox.showinfo("Success", "Book returned successfully.")
            self.load_unreturned_books()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {e}")
