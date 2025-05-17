""" database > transaction.py """
from database import get_connection


class TransactionDatabase:
    """A class to manage transactions in a database."""
    def __init__(self):
        """Initialize the transaction database."""
        self._create_transaction_table()

    def _create_transaction_table(self):
        """Creates the transactions table if it doesn't exist."""
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    issue_date TEXT NOT NULL,
                    return_date TEXT NOT NULL,
                    actual_return_date TEXT,
                    fine REAL DEFAULT 0,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (member_id) REFERENCES members (id)
                )
                """)
            conn.commit()

    def issue_book(self, book_id, member_id, issue_date, return_date):
        """Insert a new book issue record into the transactions table."""
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO transactions \
                    (book_id, member_id, issue_date, return_date)
                VALUES (?, ?, ?, ?)
                """,
                (book_id, member_id, issue_date, return_date),
            )
            conn.commit()

    def return_book(self, transaction_id, actual_return_date):
        pass

    def get_issue_book_history(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    t.id,
                    b.title AS book_title,
                    m.name AS member_name,
                    t.issue_date,
                    t.return_date,
                    t.actual_return_date,
                    t.fine
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                ORDER BY t.id DESC
            """)
        return cursor.fetchall()


transaction_db = TransactionDatabase()
