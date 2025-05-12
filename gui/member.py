""" gui > member.py """
import tkinter as tk
from tkinter import ttk
from database import MemberDatabase


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
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.member_table.bind("<<TreeviewSelect>>", self.on_member_select)

        form_frame = ttk.Frame(self.content)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=1, column=0, padx=5)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=1)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5)

        ttk.Label(form_frame, text="Phone:").grid(row=0, column=2)
        self.phone_entry = ttk.Entry(form_frame)
        self.phone_entry.grid(row=1, column=2, padx=5)

        self.load_members()

    def load_members(self):
        self.member_table.delete(*self.member_table.get_children())

        members = MemberDatabase.get_members()
        for member in members:
            self.member_table.insert("", "end", values=member)

    def on_member_select(self, event):
        selected = self.member_table.selection()
        if selected:
            item = self.member_table.item(selected[0])
            values = item["values"]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[3])
