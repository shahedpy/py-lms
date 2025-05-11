""" gui > member.py """
import tkinter as tk
from tkinter import ttk


class MemberPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(
            self.content, text="Members", font=("Arial", 14)
        )
        label.pack(pady=5)
        table_frame = ttk.Frame(self.content)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("ID", "Name", "Email", "Phone", "Created At")
        self.member_table = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )
        for col in columns:
            self.member_table.heading(col, text=col)
            self.member_table.column(col, width=100)
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.member_table.yview
        )
        self.member_table.configure(yscrollcommand=scrollbar.set)
        self.member_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
