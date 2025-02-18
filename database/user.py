""" database > user.py """
import bcrypt
from .db_connection import get_connection


def create_user_table():
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


def add_user(username, password, is_superuser=False):
    """ Add a user to the database securely with hashed password """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            print(f"Username '{username}' is already taken.")
            conn.close()
            return False

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (username, password, is_superuser) VALUES (?, ?, ?)",
            (username, hashed_password, is_superuser)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def authenticate_user(username, password):
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


create_user_table()
