""" database > member.py """
from .db_connection import get_connection


class MemberDatabase:
    def __init__(self):
        self._create_members_table()

    def _create_members_table(self):
        """Creates the members table if it doesn't exist."""
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
            conn.commit()

    def add_member(self, name, email, phone):
        """Adds a member to the members table."""
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO members (name, email, phone)
                VALUES (?, ?, ?)
                """,
                (name, email, phone)
            )
            conn.commit()

    def get_members(self):
        """Returns all members in the members table."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()

    def search_members(self, keyword):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM members
                WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
                ORDER BY created_at DESC
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
            return cursor.fetchall()

    def update_member(self, member_id, name, email, phone):
        """Updates a member in the members table."""
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE members
                SET name = ?, email = ?, phone = ?
                WHERE id = ?
                """,
                (name, email, phone, member_id)
            )
            conn.commit()

    def update_member_status(self, member_id, is_active):
        """Updates a member's active status."""
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE members
                SET is_active = ?
                WHERE id = ?
                """,
                (is_active, member_id)
            )
            conn.commit()

    def delete_member(self, member_id):
        """Deletes a member from the members table."""
        with get_connection() as conn:
            conn.execute(
                """
                DELETE FROM members
                WHERE id = ?
                """,
                (member_id,)
            )
            conn.commit()

    def total_members(self):
        """Returns the total number of members."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM members")
            return cursor.fetchone()[0]

    def get_member_by_id(self, member_id):
        """Returns a member by their ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
            return cursor.fetchone()

    def get_member_transactions(self, member_id):
        """Returns all transactions for a specific member."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, b.title, b.author, t.issue_date, t.return_date,
                       t.actual_return_date, t.fine, t.is_fine_paid
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                WHERE t.member_id = ?
                ORDER BY t.issue_date DESC
            """, (member_id,))
            return cursor.fetchall()

    def get_member_active_books(self, member_id):
        """Returns currently borrowed books for a specific member."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, b.title, b.author, t.issue_date, t.return_date
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                WHERE t.member_id = ? AND t.actual_return_date IS NULL
                ORDER BY t.issue_date DESC
            """, (member_id,))
            return cursor.fetchall()


member_db = MemberDatabase()
