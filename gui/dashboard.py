""" gui > dashboard.py """
import tkinter as tk
from tkinter import ttk


class DashboardPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(
            self.content, text="Dashboard", font=("Arial", 14)
        )
        label.pack(pady=5)
