import tkinter as tk
from gui import LibraryGUI, LoginPage


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x500")

        self.gui = LoginPage(self.root, self.show_main_ui)

    def show_main_ui(self):
        self.login_page = None
        self.gui = LibraryGUI(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
