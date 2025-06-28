""" gui > controller.py """
import tkinter as tk
from tkinter import ttk
from gui.pages import (
    DashboardPage, MemberPage, MemberDetailsPage,
    ManageBooksPage, IssueBookPage, ReturnBookPage,
    ManageUserPage,
    ChangePassPage, ReportsPage
)


class LibraryGUI:
    def __init__(self, root, on_logout):
        self.root = root

        self.on_logout = on_logout

        self.frame = ttk.Frame(self.root, padding="0")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.sidenav = ttk.Frame(self.frame, width=200, relief=tk.RAISED)
        self.sidenav.pack(side=tk.LEFT, fill=tk.Y)

        self.content = ttk.Frame(self.frame, padding="10")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_sidenav_buttons()
        self.show_dashboard()

    def create_sidenav_buttons(self):
        buttons = {
            "📊 Dashboard": self.show_dashboard,
            "👥 Manage Members": self.show_members,
            "📚 Manage Books": self.show_books,
            "📖 Issue Book": self.show_issue,
            "📘 Return Book": self.show_return,
            "👤 Manage Users": self.show_users,
            "🗒️ Reports": self.show_reports,
            "🔒 Change Password": self.show_change_pass,
        }
        for text, command in buttons.items():
            button = ttk.Button(
                self.sidenav,
                text=text,
                style="Sidenav.TButton",
                command=command
            )
            button.pack(side=tk.TOP, fill=tk.X)

        logout_button = ttk.Button(
            self.sidenav, text="Logout", command=self.logout)
        logout_button.pack(side=tk.BOTTOM, fill=tk.X, pady=0)

        style = ttk.Style()
        style.configure("Sidenav.TButton", anchor="w", padding=(10, 5))

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        DashboardPage(self.content)

    def show_members(self):
        self.clear_content()
        MemberPage(self.content, self.show_member_details)

    def show_books(self):
        """Clears content and loads the BookPage."""
        self.clear_content()
        ManageBooksPage(self.content)

    def show_issue(self):
        self.clear_content()
        IssueBookPage(self.content)

    def show_return(self):
        self.clear_content()
        ReturnBookPage(self.content)

    def show_users(self):
        self.clear_content()
        ManageUserPage(self.content)

    def show_change_pass(self):
        self.clear_content()
        ChangePassPage(self.content)

    def show_reports(self):
        self.clear_content()
        ReportsPage(self.content)

    def show_member_details(self, member_id):
        self.clear_content()
        MemberDetailsPage(self.content, member_id, self.show_members)

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


if __name__ == "__main__":
    root = tk.Tk()
    show_main_ui()
    root.mainloop()
