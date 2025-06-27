""" database > report.py """
from database import get_connection
from datetime import datetime


class ReportDatabase:
    """A class to generate various reports for the lms."""

    def __init__(self):
        """Initialize the report database."""
        pass

    def get_book_statistics(self):
        """Get overall book statistics."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_books,
                    SUM(total_copies) as total_copies,
                    SUM(available_copies) as available_copies,
                    SUM(total_copies - available_copies) as issued_copies
                FROM books
            """)
            return cursor.fetchone()

    def get_member_statistics(self):
        """Get overall member statistics."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_members,
                    COUNT(DISTINCT t.member_id) as active_members
                FROM members m
                LEFT JOIN transactions t ON m.id = t.member_id
                WHERE t.actual_return_date IS NULL 
                   OR t.actual_return_date IS NOT NULL
            """)
            result = cursor.fetchone()

            # Get members with currently issued books
            cursor = conn.execute("""
                SELECT COUNT(DISTINCT member_id) as members_with_books
                FROM transactions
                WHERE actual_return_date IS NULL
            """)
            members_with_books = cursor.fetchone()[0]

            return {
                'total_members': result[0],
                'active_members': result[1] if result[1] else 0,
                'members_with_books': members_with_books
            }

    def get_transaction_statistics(self):
        """Get transaction statistics."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_transactions,
                    SUM(CASE WHEN actual_return_date IS NULL
                        THEN 1 ELSE 0 END) as pending_returns,
                    SUM(CASE WHEN actual_return_date IS NOT NULL
                        THEN 1 ELSE 0 END) as completed_returns,
                    COALESCE(SUM(fine), 0) as total_fine_collected
                FROM transactions
            """)
            return cursor.fetchone()

    def get_overdue_books(self):
        """Get list of overdue books."""
        today = datetime.now().strftime('%Y-%m-%d')
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    t.id,
                    b.title as book_title,
                    b.author,
                    m.name as member_name,
                    m.email,
                    m.phone,
                    t.issue_date,
                    t.return_date,
                    julianday(?) - julianday(t.return_date) as days_overdue
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                WHERE t.actual_return_date IS NULL
                AND t.return_date < ?
                ORDER BY days_overdue DESC
            """, (today, today))
            return cursor.fetchall()

    def get_most_issued_books(self, limit=10):
        """Get most frequently issued books."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    b.title,
                    b.author,
                    COUNT(t.id) as issue_count,
                    b.total_copies,
                    b.available_copies
                FROM books b
                LEFT JOIN transactions t ON b.id = t.book_id
                GROUP BY b.id, b.title, b.author
                ORDER BY issue_count DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_most_active_members(self, limit=10):
        """Get most active members by number of books issued."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    m.name,
                    m.email,
                    m.phone,
                    COUNT(t.id) as books_issued,
                    SUM(CASE WHEN t.actual_return_date IS NULL
                        THEN 1 ELSE 0 END) as current_books,
                    COALESCE(SUM(t.fine), 0) as total_fine
                FROM members m
                LEFT JOIN transactions t ON m.id = t.member_id
                GROUP BY m.id, m.name, m.email
                ORDER BY books_issued DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_monthly_issue_return_report(self, months=6):
        """Get monthly issue and return statistics."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    strftime('%Y-%m', issue_date) as month,
                    COUNT(*) as books_issued,
                    SUM(CASE WHEN actual_return_date IS NOT NULL
                        THEN 1 ELSE 0 END) as books_returned,
                    COALESCE(SUM(fine), 0) as fine_collected
                FROM transactions
                WHERE issue_date >= date('now', '-{} months')
                GROUP BY strftime('%Y-%m', issue_date)
                ORDER BY month DESC
            """.format(months))
            return cursor.fetchall()

    def get_fine_report(self):
        """Get detailed fine report."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    t.id,
                    b.title as book_title,
                    m.name as member_name,
                    m.email,
                    t.return_date,
                    t.actual_return_date,
                    t.fine,
                    julianday(actual_return_date) -
                    julianday(return_date) as days_late
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                WHERE t.fine > 0
                ORDER BY t.fine DESC
            """)
            return cursor.fetchall()

    def get_books_never_issued(self):
        """Get books that have never been issued."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    b.id,
                    b.title,
                    b.author,
                    b.year,
                    b.total_copies,
                    b.created_at
                FROM books b
                LEFT JOIN transactions t ON b.id = t.book_id
                WHERE t.book_id IS NULL
                ORDER BY b.created_at DESC
            """)
            return cursor.fetchall()

    def get_daily_activity_report(self, date_str):
        """Get activity report for a specific date."""
        with get_connection() as conn:
            # Books issued on this date
            cursor = conn.execute("""
                SELECT
                    'Issue' as activity_type,
                    b.title as book_title,
                    m.name as member_name,
                    t.issue_date as activity_date
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                WHERE t.issue_date = ?

                UNION ALL

                SELECT
                    'Return' as activity_type,
                    b.title as book_title,
                    m.name as member_name,
                    t.actual_return_date as activity_date
                FROM transactions t
                JOIN books b ON t.book_id = b.id
                JOIN members m ON t.member_id = m.id
                WHERE t.actual_return_date = ?

                ORDER BY activity_date
            """, (date_str, date_str))
            return cursor.fetchall()


report_db = ReportDatabase()
