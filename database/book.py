""" database > book.py """

from database import get_connection


def create_books_table():
    """Creates the books table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        conn.commit()


def add_book(title, author, year, price):
    """Adds a book to the books table."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO books (title, author, year, price)
            VALUES (?, ?, ?, ?)
            """,
            (title, author, year, price)
        )
        conn.commit()


def get_books():
    """Returns all books in the books table."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()


def update_book(book_id, title, author, year):
    """Updates a book in the books table."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE books
            SET title = ?, author = ?, year = ?
            WHERE id = ?
            """,
            (title, author, year, book_id)
        )
        conn.commit()


create_books_table()
