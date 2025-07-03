import sys
import tkinter as tk
from gui import LibraryGUI
from gui.pages import LoginPage
from database.createsuperuser import create_superuser
from database.resetpassword import reset_password


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x700")

        self.show_login_page()

    def show_login_page(self):
        self.gui = LoginPage(self.root, self.show_main_ui)

    def show_main_ui(self):
        if self.gui.frame:
            self.gui.frame.destroy()

        self.gui = LibraryGUI(self.root, self.show_login_page)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "createsuperuser":
            create_superuser()
            sys.exit(0)
        elif command == "resetpassword":
            reset_password()
            sys.exit(0)
        else:
            print(f"Unknown command: {command}")
            print("Available commands:")
            print("  createsuperuser - Create a new superuser")
            print("  resetpassword   - Reset a user's password")
            sys.exit(1)

    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
