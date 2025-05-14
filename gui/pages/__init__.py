""" gui > pages > __init__.py """

from .login import LoginPage
from .dashboard import DashboardPage
from .member import MemberPage
from .manage_books import ManageBooksPage
from .issue_book import IssueBookPage
from .return_book import ReturnBookPage
from .settings import SettingsPage


__all__ = [
    LoginPage,
    DashboardPage,
    MemberPage,
    ManageBooksPage,
    IssueBookPage,
    ReturnBookPage,
    SettingsPage
]
