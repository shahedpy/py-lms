""" gui > pages > __init__.py """

from .login import LoginPage
from .dashboard import DashboardPage
from .manage_members import MemberPage
from .member_details import MemberDetailsPage
from .manage_books import ManageBooksPage
from .issue_book import IssueBookPage
from .return_book import ReturnBookPage
from .manage_users import ManageUserPage
from .change_password import ChangePassPage
from .reports import ReportsPage


__all__ = [
    LoginPage,
    DashboardPage,
    MemberPage,
    MemberDetailsPage,
    ManageBooksPage,
    IssueBookPage,
    ReturnBookPage,
    ManageUserPage,
    ChangePassPage,
    ReportsPage
]
