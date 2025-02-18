""" gui > main_ui.py """
import tkinter as tk
from tkinter import ttk


class LibraryGUI:
    def __init__(self, root, on_logout):
        self.root = root

        self.on_logout = on_logout

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

        logout_button = ttk.Button(
            self.sidenav, text="Logout", command=self.logout)
        logout_button.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def logout(self):
        self.frame.destroy()
        self.on_logout()


def show_login_page():
    for widget in root.winfo_children():
        widget.destroy()

    login_label = ttk.Label(root, text="Login Page")
    login_label.pack(pady=20)

    back_button = ttk.Button(
        root, text="Back to Main UI", command=show_main_ui)
    back_button.pack(pady=10)


def show_main_ui():
    for widget in root.winfo_children():
        widget.destroy()
    app = LibraryGUI(root, on_logout=show_login_page)


if __name__ == "__main__":
    root = tk.Tk()
    show_main_ui()
    root.mainloop()
