""" gui > pages > member_details.py """
import tkinter as tk
from tkinter import ttk, messagebox
from database import member_db


class MemberDetailsPage:
    def __init__(self, parent_frame, member_id, on_back):
        self.parent_frame = parent_frame
        self.member_id = member_id
        self.on_back = on_back
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.member_data = None
        self.create_widgets()
        self.load_member_details()

    def create_widgets(self):
        # Header with back button
        header_frame = ttk.Frame(self.content)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        back_button = ttk.Button(
            header_frame, text="← Back", command=self.on_back
        )
        back_button.pack(side=tk.LEFT)

        ttk.Label(
            header_frame, text="👤 Member Details", font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Main content frame
        main_frame = ttk.Frame(self.content)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Member information section
        info_frame = ttk.LabelFrame(
            main_frame, text="Member Information", padding="10"
        )
        info_frame.pack(fill=tk.X, pady=(0, 10))

        # Member details labels
        self.name_label = ttk.Label(
            info_frame, text="Name: Loading...", font=("Arial", 12)
        )
        self.name_label.grid(row=0, column=0, sticky="w", padx=(0, 20))

        self.email_label = ttk.Label(
            info_frame, text="Email: Loading...", font=("Arial", 12)
        )
        self.email_label.grid(row=0, column=1, sticky="w")

        self.phone_label = ttk.Label(
            info_frame, text="Phone: Loading...", font=("Arial", 12)
        )
        self.phone_label.grid(
            row=1, column=0, sticky="w", padx=(0, 20), pady=(5, 0)
        )

        self.created_label = ttk.Label(
            info_frame, text="Member Since: Loading...", font=("Arial", 12)
        )
        self.created_label.grid(row=1, column=1, sticky="w", pady=(5, 0))

        self.status_label = ttk.Label(
            info_frame, text="Status: Loading...", font=("Arial", 12)
        )
        self.status_label.grid(row=2, column=0, sticky="w", pady=(5, 0))

        # Currently borrowed books section
        borrowed_frame = ttk.LabelFrame(
            main_frame, text="Currently Borrowed Books", padding="10"
        )
        borrowed_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create treeview for borrowed books
        borrowed_columns = ("ID", "Title", "Author", "Issue Date", "Due Date")
        self.borrowed_tree = ttk.Treeview(
            borrowed_frame, columns=borrowed_columns, show="headings", height=6
        )

        for col in borrowed_columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=100)

        # Scrollbar for borrowed books
        borrowed_scrollbar = ttk.Scrollbar(
            borrowed_frame, orient="vertical", command=self.borrowed_tree.yview
        )
        self.borrowed_tree.configure(yscrollcommand=borrowed_scrollbar.set)

        self.borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        borrowed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Transaction history section
        history_frame = ttk.LabelFrame(
            main_frame, text="Transaction History", padding="10"
        )
        history_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview for transaction history
        history_columns = (
            "ID", "Title", "Author", "Issue Date", "Due Date",
            "Return Date", "Fine"
        )
        self.history_tree = ttk.Treeview(
            history_frame, columns=history_columns, show="headings", height=8
        )

        for col in history_columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        # Scrollbar for history
        history_scrollbar = ttk.Scrollbar(
            history_frame, orient="vertical", command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_member_details(self):
        """Load member details and populate the widgets."""
        try:
            self.member_data = member_db.get_member_by_id(self.member_id)

            if not self.member_data:
                messagebox.showerror("Error", "Member not found!")
                self.on_back()
                return

            self.name_label.config(text=f"Name: {self.member_data[1]}")
            self.email_label.config(text=f"Email: {self.member_data[2]}")
            self.phone_label.config(text=f"Phone: {self.member_data[3]}")

            is_active = (
                self.member_data[4]
                if len(self.member_data) > 4 else True
            )
            status = "Active" if is_active else "Inactive"
            self.status_label.config(text=f"Status: {status}")

            self.load_borrowed_books()

            self.load_transaction_history()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load member details: {str(e)}"
            )
            self.on_back()

    def load_borrowed_books(self):
        """Load currently borrowed books."""
        try:
            self.borrowed_tree.delete(*self.borrowed_tree.get_children())
            active_books = member_db.get_member_active_books(self.member_id)
            for book in active_books:
                self.borrowed_tree.insert("", "end", values=book)
            if not active_books:
                self.borrowed_tree.insert(
                    "", "end",
                    values=("", "No books currently borrowed", "", "", "")
                )

        except Exception as e:
            print(f"Error loading borrowed books: {str(e)}")

    def load_transaction_history(self):
        """Load transaction history."""
        try:
            self.history_tree.delete(*self.history_tree.get_children())
            transactions = member_db.get_member_transactions(self.member_id)
            for transaction in transactions:
                # Format the return date
                return_date = (
                    transaction[5] if transaction[5] else "Not Returned"
                )
                fine = (
                    f"${transaction[6]:.2f}"
                    if transaction[6] and transaction[6] > 0
                    else "No Fine"
                )
                formatted_transaction = (
                    transaction[0], transaction[1], transaction[2],
                    transaction[3], transaction[4], return_date, fine
                )
                self.history_tree.insert(
                    "", "end", values=formatted_transaction
                )
            if not transactions:
                self.history_tree.insert(
                    "", "end",
                    values=("", "No transaction history", "", "", "", "", "")
                )

        except Exception as e:
            print(f"Error loading transaction history: {str(e)}")
