""" gui > dashboard.py """
import tkinter as tk
from tkinter import ttk


class DashboardPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding=20)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(
            self.content, text="📊 Dashboard", font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Info frame
        info_frame = ttk.Frame(self.content)
        info_frame.pack(fill=tk.BOTH, expand=True)

        # Helper function to create metric blocks
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

        # Metrics
        self.total_books_label = create_stat_box(info_frame, "📚", "Total Books", 0)
        self.total_members_label = create_stat_box(info_frame, "👥", "Total Members", 0)
        self.total_transactions_label = create_stat_box(info_frame, "💳", "Total Transactions", 0)
        self.total_users_label = create_stat_box(info_frame, "🧑‍💻", "Total Users", 0)

    # Optional: Add methods to update metrics dynamically
    def update_stats(self, books=0, members=0, transactions=0, users=0):
        self.total_books_label.config(text=f"📚 Total Books: {books}")
        self.total_members_label.config(text=f"👥 Total Members: {members}")
        self.total_transactions_label.config(text=f"💳 Total Transactions: {transactions}")
        self.total_users_label.config(text=f"🧑‍💻 Total Users: {users}")
