""" database > book.py """
from .db_connection import get_connection


class BookDatabase:
    def __init__(self):
        self._create_books_table()

    def _create_books_table(self):
        """Creates the books table if it doesn't exist."""
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    price REAL NOT NULL,
                    total_copies INTEGER DEFAULT 0,
                    available_copies INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
            conn.commit()

    def add_book(self, title, author, year, price, total_copies):
        """Adds a book to the books table."""
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO books (
                    title, author, year, price, total_copies, available_copies
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, author, year, price, total_copies, total_copies)
            )
            conn.commit()

    def get_books(self):
        """Returns all books in the books table."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()

    def search_books(self, keyword):
        """Searches books by title or author."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()

    def update_book(self, book_id, title, author, year, price):
        """Updates a book in the books table."""
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE books
                SET title = ?, author = ?, year = ?, price = ?
                WHERE id = ?
                """,
                (title, author, year, price, book_id)
            )
            conn.commit()

    def delete_book(self, book_id):
        """Deletes a book from the books table."""
        with get_connection() as conn:
            conn.execute(
                """
                DELETE FROM books
                WHERE id = ?
                """,
                (book_id,)
            )
            conn.commit()

    def total_books(self):
        """Returns the total number of books in the books table."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM books")
            return cursor.fetchone()[0]


book_db = BookDatabase()
