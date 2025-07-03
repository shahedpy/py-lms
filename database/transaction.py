""" database > transaction.py """
from .db_connection import get_connection
from datetime import date


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
                    is_fine_paid BOOLEAN DEFAULT 0,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (member_id) REFERENCES members (id)
                )
                """)
            conn.commit()

    def issue_book(self, book_id, member_id, issue_date, return_date):
        """Insert a new book issue record into the transactions table."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id = ?
            """, (book_id,))

            conn.execute(
                """
                INSERT INTO transactions \
                    (book_id, member_id, issue_date, return_date)
                VALUES (?, ?, ?, ?)
                """,
                (book_id, member_id, issue_date, return_date),
            )
            conn.commit()

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
                    t.fine,
                    t.is_fine_paid
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                ORDER BY t.id DESC
            """)
        return cursor.fetchall()

    def return_book(self, transaction_id, actual_return_date):
        """Update the transaction with actual \
              return date and calculate fine."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT return_date FROM transactions
                WHERE id = ? AND actual_return_date IS NULL
            """, (transaction_id,))
            row = cursor.fetchone()

            if row is None:
                raise Exception(
                    "Invalid transaction ID or book already returned.")

            return_date = row[0]
            fine = 0
            if actual_return_date > return_date:
                days_late = (date.fromisoformat(actual_return_date) -
                             date.fromisoformat(return_date)).days
                fine = days_late * 10

            conn.execute("""
                UPDATE books
                SET available_copies = available_copies + 1
                WHERE id = (SELECT book_id FROM transactions WHERE id = ?)
            """, (transaction_id,))

            conn.execute("""
                UPDATE transactions
                SET actual_return_date = ?, fine = ?
                WHERE id = ?
            """, (actual_return_date, fine, transaction_id))
            conn.commit()

    def book_issue_count(self):
        """Returns the total number of issued books."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM transactions
            """)
            return cursor.fetchone()[0]

    def book_return_count(self):
        """Returns the total number of returned books."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM transactions
                WHERE actual_return_date IS NOT NULL
            """)
            return cursor.fetchone()[0]

    def books_on_member_hand(self):
        """Returns the total number of books on members hand."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM transactions
                WHERE actual_return_date IS NULL
            """)
            return cursor.fetchone()[0]

    def total_fine(self):
        """Returns total fine"""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT SUM(fine) FROM transactions
                WHERE actual_return_date IS NOT NULL
            """)
            return cursor.fetchone()[0]

    def mark_fine_as_paid(self, transaction_id):
        """Mark a fine as paid for a specific transaction."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE transactions
                SET is_fine_paid = 1
                WHERE id = ? AND fine > 0
            """, (transaction_id,))
            conn.commit()

    def mark_fine_as_unpaid(self, transaction_id):
        """Mark a fine as unpaid for a specific transaction."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE transactions
                SET is_fine_paid = 0
                WHERE id = ? AND fine > 0
            """, (transaction_id,))
            conn.commit()

    def get_unpaid_fines(self):
        """Get all transactions with unpaid fines."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    t.id,
                    b.title AS book_title,
                    m.name AS member_name,
                    m.email,
                    m.phone,
                    t.return_date,
                    t.actual_return_date,
                    t.fine,
                    t.is_fine_paid
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                WHERE t.fine > 0 AND t.is_fine_paid = 0
                ORDER BY t.actual_return_date DESC
            """)
            return cursor.fetchall()

    def get_paid_fines(self):
        """Get all transactions with paid fines."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    t.id,
                    b.title AS book_title,
                    m.name AS member_name,
                    m.email,
                    m.phone,
                    t.return_date,
                    t.actual_return_date,
                    t.fine,
                    t.is_fine_paid
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                WHERE t.fine > 0 AND t.is_fine_paid = 1
                ORDER BY t.actual_return_date DESC
            """)
            return cursor.fetchall()

    def total_unpaid_fine(self):
        """Returns total unpaid fine amount."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT SUM(fine) FROM transactions
                WHERE fine > 0 AND is_fine_paid = 0
            """)
            result = cursor.fetchone()[0]
            return result if result else 0

    def total_paid_fine(self):
        """Returns total paid fine amount."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT SUM(fine) FROM transactions
                WHERE fine > 0 AND is_fine_paid = 1
            """)
            result = cursor.fetchone()[0]
            return result if result else 0


transaction_db = TransactionDatabase()
