""" gui > pages > setting.py """
import tkinter as tk
from tkinter import ttk
from database import change_password


class SettingsPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self.content, text="⚙️ Settings", font=("Arial", 14)
        ).pack(pady=5)

        self.old_pass_var = tk.StringVar()
        self.new_pass_var = tk.StringVar()
        self.confirm_pass_var = tk.StringVar()
        self.username_var = tk.StringVar()

        ttk.Label(self.content, text="Username:").pack(pady=(10, 0))
        ttk.Entry(self.content, textvariable=self.username_var).pack()

        ttk.Label(self.content, text="Old Password:").pack(pady=(10, 0))
        ttk.Entry(
            self.content, textvariable=self.old_pass_var, show="*").pack()

        ttk.Label(self.content, text="New Password:").pack(pady=(10, 0))
        ttk.Entry(
            self.content, textvariable=self.new_pass_var, show="*").pack()

        ttk.Label(
            self.content, text="Confirm New Password:").pack(pady=(10, 0))
        ttk.Entry(
            self.content, textvariable=self.confirm_pass_var, show="*").pack()

        ttk.Button(
            self.content,
            text="Change Password",
            command=self.handle_change_password
        ).pack(pady=10)

        self.message_label = ttk.Label(self.content, text="")
        self.message_label.pack()

    def handle_change_password(self):
        username = self.username_var.get()
        old_pass = self.old_pass_var.get()
        new_pass = self.new_pass_var.get()
        confirm_pass = self.confirm_pass_var.get()

        if new_pass != confirm_pass:
            self.message_label.config(
                text="New passwords do not match.", foreground="red")
            return

        success, message = change_password(username, old_pass, new_pass)
        color = "green" if success else "red"
        self.message_label.config(text=message, foreground=color)
        self.clear_entries()

    def clear_entries(self):
        self.old_pass_var.set("")
        self.new_pass_var.set("")
        self.confirm_pass_var.set("")
        self.username_var.set("")
