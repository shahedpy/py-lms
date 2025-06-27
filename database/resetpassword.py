""" database/createsuperuser.py """
import sys
import os
import getpass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.user import user_db # noqa


def reset_password():
    """ reset a user's password """
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    if password != password_confirm:
        print("Passwords do not match!")
        return
    if user_db.reset_password(username, password):
        print(f"Password for user '{username}' reset successfully!")
    else:
        print("Error adding superuser!")


if __name__ == "__main__":
    reset_password()
