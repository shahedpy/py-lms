import tkinter as tk
from gui import LibraryGUI
from gui.pages import LoginPage


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x600")

        self.show_login_page()

    def show_login_page(self):
        self.gui = LoginPage(self.root, self.show_main_ui)

    def show_main_ui(self):
        if self.gui.frame:
            self.gui.frame.destroy()

        self.gui = LibraryGUI(self.root, self.show_login_page)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
