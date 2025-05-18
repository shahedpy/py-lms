""" gui > pages > dashboard.py """
import tkinter as tk
from tkinter import ttk
from database import book_db, member_db, transaction_db, total_users


class DashboardPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding=0)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self.content, text="📊 Dashboard", font=("Arial", 16, "bold")
        ).pack(pady=10)

        info_frame = ttk.Frame(self.content)
        info_frame.pack(fill=tk.BOTH, expand=True)

        def create_stat_box(parent, emoji, title, value):
            box = ttk.Frame(parent, padding=10, relief=tk.RIDGE, borderwidth=2)
            box.pack(fill=tk.X, pady=5)

            label = ttk.Label(
                box,
                text=f"{emoji} {title}: {value}",
                font=("Arial", 12, "bold"),
                anchor="w"
            )
            label.pack(fill=tk.X)
            return label

        self.total_members_label = create_stat_box(
            info_frame, "👥", "Total Members",
            member_db.total_members())
        self.total_books_label = create_stat_box(
            info_frame, "📚", "Total Books",
            book_db.total_books())
        self.book_issued_label = create_stat_box(
            info_frame, "📖", "Book Issued",
            transaction_db.book_issue_count())
        self.book_returned_label = create_stat_box(
            info_frame, "📘", "Book Returned",
            transaction_db.book_return_count())
        self.book_on_members_hand_label = create_stat_box(
            info_frame, "📗", "Books on Member's Hand",
            transaction_db.books_on_member_hand())
        self.total_transactions_label = create_stat_box(
            info_frame, "💳", "Total Fine",
            transaction_db.total_fine())
        self.total_users_label = create_stat_box(
            info_frame, "🧑", "Total Users", total_users())

    def update_stats(self, books=0, members=0, transactions=0, users=0):
        self.total_books_label.config(text=f"📚 Total Books: {books}")
        self.total_members_label.config(text=f"👥 Total Members: {members}")
        self.total_transactions_label.config(
            text=f"💳 Total Transactions: {transactions}")
        self.total_users_label.config(text=f"🧑‍💻 Total Users: {users}")
