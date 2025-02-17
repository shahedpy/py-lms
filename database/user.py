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
        is_active BOOLEAN DEFAULT 1
    )
    """)
    conn.commit()
    conn.close()
    print("User table created successfully!")


def add_user(username, password):
    """ Add a user to the database securely with hashed password """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
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
