""" database > user.py """
import bcrypt
from .db_connection import get_connection


class UserDatabase:
    def __init__(self):
        """ Initialize the user database """
        self._create_user_table()

    def _create_user_table(self):
        """ Create the user table if it doesn't exist """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            is_superuser BOOLEAN DEFAULT 0
        )
        """)
        conn.commit()
        conn.close()

    def add_user(self, username, password, is_superuser=False):
        """ Add a user to the database securely with hashed password """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE username = ?", (username,)
            )
            user_count = cursor.fetchone()[0]
            if user_count > 0:
                print(f"Username '{username}' is already taken.")
                conn.close()
                return False

            hashed_password = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt())

            cursor.execute(
                "INSERT INTO users (username, password, is_superuser) VALUES (?, ?, ?)", # noqa
                (username, hashed_password, is_superuser)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def authenticate_user(self, username, password):
        """ Authenticate a user with a hashed password """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ? AND is_active = 1",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_hashed_password = user[0]
            return bcrypt.checkpw(password.encode(), stored_hashed_password)

    def change_password(self, username, old_password, new_password):
        """Change a user's password after verifying the old one."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ? AND is_active = 1",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            conn.close()
            return False, "User not found or inactive."

        stored_hashed_password = user[0]

        if not bcrypt.checkpw(old_password.encode(), stored_hashed_password):
            conn.close()
            return False, "Old password is incorrect."

        new_hashed_password = bcrypt.hashpw(
            new_password.encode(), bcrypt.gensalt())
        cursor.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_hashed_password, username)
        )
        conn.commit()
        conn.close()
        return True, "Password changed successfully."

    def reset_password(self, username, new_password):
        """Reset a user's password without requiring the old password."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            user = cursor.fetchone()

            if not user:
                conn.close()
                return False, "User not found or inactive."

            new_hashed_password = bcrypt.hashpw(
                new_password.encode(), bcrypt.gensalt())

            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_hashed_password, username)
            )
            conn.commit()
            conn.close()
            return True, "Password reset successfully."

        except Exception as e:
            print(f"Error resetting password: {e}")
            return False, "An error occurred while resetting the password."

    def total_users(self):
        """ Returns the total number of users """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        conn.close()
        return total


user_db = UserDatabase()
