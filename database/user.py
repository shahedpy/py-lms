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
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT COUNT(*) FROM users WHERE username = ?", (username,)
                )
                user_count = cursor.fetchone()[0]
                if user_count > 0:
                    print(f"Username '{username}' is already taken.")
                    return False

                hashed_password = bcrypt.hashpw(
                    password.encode(), bcrypt.gensalt())

                cursor.execute(
                    "INSERT INTO users (username, password, is_superuser) VALUES (?, ?, ?)", # noqa
                    (username, hashed_password, is_superuser)
                )
                conn.commit()
                return True
        except Exception as e:
            print(e)
            return False

    def authenticate_user(self, username, password):
        """ Authenticate a user with a hashed password """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user[0]
                return bcrypt.checkpw(password.encode(), stored_hashed_password)

    def change_password(self, username, old_password, new_password):
        """Change a user's password after verifying the old one."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            user = cursor.fetchone()

            if not user:
                return False, "User not found or inactive."

            stored_hashed_password = user[0]

            if not bcrypt.checkpw(old_password.encode(), stored_hashed_password):
                return False, "Old password is incorrect."

            new_hashed_password = bcrypt.hashpw(
                new_password.encode(), bcrypt.gensalt())
            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_hashed_password, username)
            )
            conn.commit()
            return True, "Password changed successfully."

    def reset_password(self, username, new_password):
        """Reset a user's password without requiring the old password."""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT id FROM users WHERE username = ? AND is_active = 1",
                    (username,)
                )
                user = cursor.fetchone()

                if not user:
                    return False, "User not found or inactive."

                new_hashed_password = bcrypt.hashpw(
                    new_password.encode(), bcrypt.gensalt())

                cursor.execute(
                    "UPDATE users SET password = ? WHERE username = ?",
                    (new_hashed_password, username)
                )
                conn.commit()
                return True, "Password reset successfully."

        except Exception as e:
            print(f"Error resetting password: {e}")
            return False, "An error occurred while resetting the password."

    def total_users(self):
        """ Returns the total number of users """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]
            return total

    def get_users(self):
        """ Get all users from the database """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, is_active, is_superuser
                FROM users
                ORDER BY id
            """)
            users = cursor.fetchall()
            return users

    def search_users(self, keyword):
        """ Search users by username """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, is_active, is_superuser
                FROM users
                WHERE username LIKE ?
                ORDER BY id
            """, (f"%{keyword}%",))
            users = cursor.fetchall()
            return users

    def update_user_status(self, user_id, is_active):
        """ Update user active status """
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET is_active = ? WHERE id = ?",
                    (is_active, user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user status: {e}")
            return False

    def update_user_role(self, user_id, is_superuser):
        """ Update user superuser status """
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET is_superuser = ? WHERE id = ?",
                    (is_superuser, user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False

    def delete_user(self, user_id):
        """ Delete a user from the database """
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False


user_db = UserDatabase()
