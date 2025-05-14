""" database/createsuperuser.py """
import sys
import os
import getpass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.user import add_user # noqa


def create_superuser():
    """ Add a superuser to the database """
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    if password != password_confirm:
        print("Passwords do not match!")
        return
    if add_user(username, password, is_superuser=True):
        print(f"Superuser '{username}' created successfully!")
    else:
        print("Error adding superuser!")


if __name__ == "__main__":
    create_superuser()
