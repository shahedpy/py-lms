""" gui > pages > manage_members.py """
import tkinter as tk
from tkinter import ttk
from database import member_db


class MemberPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self.content, text="👥 Manage Members", font=("Arial", 16, "bold")
        ).pack(pady=5)

        search_frame = ttk.Frame(self.content)
        search_frame.pack(pady=5)

        ttk.Label(
            search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(
            search_frame, text="Search", command=self.search_members)
        search_button.pack(side=tk.LEFT, padx=5)

        reset_button = ttk.Button(
            search_frame, text="Reset", command=self.reset_search)
        reset_button.pack(side=tk.LEFT, padx=5)

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

        button_frame = ttk.Frame(self.content)
        button_frame.pack(pady=10)

        self.add_button = ttk.Button(
            button_frame, text="Add Member", command=self.submit_member
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.load_members()

    def load_members(self):
        self.member_table.delete(*self.member_table.get_children())

        members = member_db.get_members()
        for member in members:
            self.member_table.insert("", "end", values=member)

    def search_members(self):
        search_term = self.search_entry.get()
        if search_term:
            self.member_table.delete(*self.member_table.get_children())
            members = member_db.search_members(search_term)
            for member in members:
                self.member_table.insert("", "end", values=member)

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_members()

    def submit_member(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        if name and email and phone:
            member_db.add_member(name, email, phone)
            self.load_members()
            self.clear_entries()

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

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
