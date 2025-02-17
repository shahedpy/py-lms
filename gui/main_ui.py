""" gui > main_ui.py """
import tkinter as tk
from tkinter import ttk


class LibraryGUI:
    def __init__(self, root):
        self.root = root

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.sidenav = ttk.Frame(self.frame, width=200, relief=tk.RAISED)
        self.sidenav.pack(side=tk.LEFT, fill=tk.Y)

        self.content = ttk.Frame(self.frame, padding="10")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_sidenav_buttons()

    def create_sidenav_buttons(self):
        buttons = ["Home", "Books", "Members", "Issue", "Return", "Settings"]
        for button_text in buttons:
            button = ttk.Button(self.sidenav, text=button_text)
            button.pack(side=tk.TOP, fill=tk.X)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
