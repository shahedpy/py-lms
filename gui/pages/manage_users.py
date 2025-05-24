""" gui > pages > manage_users.py """
import tkinter as tk
from tkinter import ttk


class ManageUserPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self.content, text="👥 Manage Users", font=("Arial", 16, "bold")
        ).pack(pady=5)
