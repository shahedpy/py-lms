""" gui > pages > __init__.py """

from .login import LoginPage
from .dashboard import DashboardPage
from .book import BookPage
from .member import MemberPage
from .issue_book import IssueBookPage
from .return_book import ReturnBookPage
from .settings import SettingsPage


__all__ = [
    LoginPage,
    DashboardPage,
    BookPage,
    MemberPage,
    IssueBookPage,
    ReturnBookPage,
    SettingsPage
]
