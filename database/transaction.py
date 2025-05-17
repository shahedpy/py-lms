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

    def get_all_transactions(self):
        pass


transaction_db = TransactionDatabase()
