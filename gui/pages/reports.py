""" gui > pages > reports.py """
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database.report import report_db
import csv
import os


class ReportsPage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the reports user interface."""
        title_label = ttk.Label(
            self.frame,
            text="📊 Library Reports",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Create notebook for different report categories
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add different report tabs
        self.create_overview_tab()
        self.create_books_tab()
        self.create_members_tab()
        self.create_transactions_tab()
        self.create_fines_tab()

    def create_overview_tab(self):
        """Create overview statistics tab."""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📈 Overview")

        # Statistics cards frame
        stats_frame = ttk.Frame(overview_frame)
        stats_frame.pack(fill=tk.X, pady=10)

        # Create statistics cards
        self.create_stats_cards(stats_frame)

        # Monthly trend chart frame
        trend_frame = ttk.LabelFrame(overview_frame, text="Monthly Activity")
        trend_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.create_monthly_trend(trend_frame)

    def create_stats_cards(self, parent):
        """Create statistics cards."""
        # Get statistics
        book_stats = report_db.get_book_statistics()
        member_stats = report_db.get_member_statistics()
        transaction_stats = report_db.get_transaction_statistics()

        # Books statistics
        books_frame = ttk.LabelFrame(parent, text="📚 Books")
        books_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(books_frame, text=f"Total Books: {book_stats[0]}",
                  font=("Arial", 12, "bold")).pack(pady=2)
        ttk.Label(books_frame, text=f"Total Copies: {book_stats[1]}").pack()
        ttk.Label(books_frame, text=f"Available: {book_stats[2]}").pack()
        ttk.Label(books_frame, text=f"Issued: {book_stats[3]}").pack()

        # Members statistics
        members_frame = ttk.LabelFrame(parent, text="👥 Members")
        members_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(members_frame,
                  text=f"Total Members: {member_stats['total_members']}",
                  font=("Arial", 12, "bold")).pack(pady=2)
        ttk.Label(members_frame,
                  text=f"Active Members: {member_stats['active_members']}"
                  ).pack()
        ttk.Label(members_frame,
                  text=f"With Books: {member_stats['members_with_books']}"
                  ).pack()

        # Transactions statistics
        trans_frame = ttk.LabelFrame(parent, text="📖 Transactions")
        trans_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(trans_frame,
                  text=f"Total: {transaction_stats[0]}",
                  font=("Arial", 12, "bold")).pack(pady=2)
        ttk.Label(trans_frame,
                  text=f"Pending: {transaction_stats[1]}").pack()
        ttk.Label(trans_frame,
                  text=f"Completed: {transaction_stats[2]}").pack()
        ttk.Label(trans_frame,
                  text=f"Fine Collected: ${transaction_stats[3]:.2f}"
                  ).pack()

    def create_monthly_trend(self, parent):
        """Create monthly trend display."""
        # Controls frame
        controls = ttk.Frame(parent)
        controls.pack(fill=tk.X, pady=5)

        ttk.Label(controls, text="Months:").pack(side=tk.LEFT)
        months_var = tk.StringVar(value="6")
        months_combo = ttk.Combobox(controls, textvariable=months_var,
                                    values=["3", "6", "12"], width=5,
                                    state="readonly")
        months_combo.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(controls, text="Refresh",
                                 command=lambda: self.load_monthly_data(
                                     int(months_var.get()), tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Treeview for monthly data
        columns = ("Month", "Books Issued", "Books Returned", "Fine Collected")
        tree = ttk.Treeview(parent, columns=columns, show="headings",
                            height=8)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial data
        self.load_monthly_data(6, tree)

    def load_monthly_data(self, months, tree):
        """Load monthly trend data."""
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)

        # Get and display monthly data
        monthly_data = report_db.get_monthly_issue_return_report(months)
        for row in monthly_data:
            tree.insert("", tk.END, values=row)

    def create_books_tab(self):
        """Create books reports tab."""
        books_frame = ttk.Frame(self.notebook)
        self.notebook.add(books_frame, text="📚 Books")

        # Sub-tabs for different book reports
        book_notebook = ttk.Notebook(books_frame)
        book_notebook.pack(fill=tk.BOTH, expand=True)

        # Most issued books
        self.create_most_issued_books_tab(book_notebook)

        # Never issued books
        self.create_never_issued_books_tab(book_notebook)

    def create_most_issued_books_tab(self, parent):
        """Create most issued books report."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Most Issued")

        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=5)

        ttk.Label(controls, text="Top:").pack(side=tk.LEFT)
        limit_var = tk.StringVar(value="10")
        limit_combo = ttk.Combobox(controls, textvariable=limit_var,
                                   values=["5", "10", "20", "50"], width=5,
                                   state="readonly")
        limit_combo.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(
            controls, text="Refresh",
            command=lambda: self.load_most_issued_books(
                int(limit_var.get()), tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            controls, text="Export CSV",
            command=lambda: self.export_treeview_to_csv(
                tree, "most_issued_books.csv"))
        export_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("Title", "Author", "Issue Count", "Total Copies",
                   "Available")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial data
        self.load_most_issued_books(10, tree)

    def load_most_issued_books(self, limit, tree):
        """Load most issued books data."""
        for item in tree.get_children():
            tree.delete(item)

        data = report_db.get_most_issued_books(limit)
        for row in data:
            tree.insert("", tk.END, values=row)

    def create_never_issued_books_tab(self, parent):
        """Create never issued books report."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Never Issued")

        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=5)

        refresh_btn = ttk.Button(
            controls, text="Refresh",
            command=lambda: self.load_never_issued_books(tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            controls, text="Export CSV",
            command=lambda: self.export_treeview_to_csv(
                tree, "never_issued_books.csv"))
        export_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("ID", "Title", "Author", "Year", "Total Copies",
                   "Added Date")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial data
        self.load_never_issued_books(tree)

    def load_never_issued_books(self, tree):
        """Load never issued books data."""
        for item in tree.get_children():
            tree.delete(item)

        data = report_db.get_books_never_issued()
        for row in data:
            tree.insert("", tk.END, values=row)

    def create_members_tab(self):
        """Create members reports tab."""
        members_frame = ttk.Frame(self.notebook)
        self.notebook.add(members_frame, text="👥 Members")

        # Controls
        controls = ttk.Frame(members_frame)
        controls.pack(fill=tk.X, pady=5)

        ttk.Label(controls, text="Top Active Members:").pack(side=tk.LEFT)
        limit_var = tk.StringVar(value="10")
        limit_combo = ttk.Combobox(controls, textvariable=limit_var,
                                   values=["5", "10", "20", "50"], width=5,
                                   state="readonly")
        limit_combo.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(
            controls, text="Refresh",
            command=lambda: self.load_active_members(
                int(limit_var.get()), tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            controls, text="Export CSV",
            command=lambda: self.export_treeview_to_csv(
                tree, "active_members.csv"))
        export_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("Name", "Email", "Phone", "Books Issued",
                   "Current Books", "Total Fine")
        tree = ttk.Treeview(members_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(members_frame, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial data
        self.load_active_members(10, tree)

    def load_active_members(self, limit, tree):
        """Load most active members data."""
        for item in tree.get_children():
            tree.delete(item)

        data = report_db.get_most_active_members(limit)
        for row in data:
            tree.insert("", tk.END, values=row)

    def create_transactions_tab(self):
        """Create transactions reports tab."""
        trans_frame = ttk.Frame(self.notebook)
        self.notebook.add(trans_frame, text="📖 Transactions")

        # Sub-tabs for transaction reports
        trans_notebook = ttk.Notebook(trans_frame)
        trans_notebook.pack(fill=tk.BOTH, expand=True)

        # Overdue books
        self.create_overdue_books_tab(trans_notebook)

        # Daily activity
        self.create_daily_activity_tab(trans_notebook)

    def create_overdue_books_tab(self, parent):
        """Create overdue books report."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Overdue Books")

        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=5)

        refresh_btn = ttk.Button(
            controls, text="Refresh",
            command=lambda: self.load_overdue_books(tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            controls, text="Export CSV",
            command=lambda: self.export_treeview_to_csv(
                tree, "overdue_books.csv"))
        export_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("ID", "Book Title", "Author", "Member", "Email",
                   "Phone", "Issue Date", "Due Date", "Days Overdue")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial data
        self.load_overdue_books(tree)

    def load_overdue_books(self, tree):
        """Load overdue books data."""
        for item in tree.get_children():
            tree.delete(item)

        data = report_db.get_overdue_books()
        for row in data:
            # Format days overdue
            formatted_row = list(row)
            formatted_row[8] = f"{int(row[8])}" if row[8] else "0"
            tree.insert("", tk.END, values=formatted_row)

    def create_daily_activity_tab(self, parent):
        """Create daily activity report."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Daily Activity")

        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=5)

        ttk.Label(controls, text="Date:").pack(side=tk.LEFT)
        date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(controls, textvariable=date_var, width=12)
        date_entry.pack(side=tk.LEFT, padx=5)

        search_btn = ttk.Button(
            controls, text="Search",
            command=lambda: self.load_daily_activity(date_var.get(), tree))
        search_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            controls, text="Export CSV",
            command=lambda: self.export_treeview_to_csv(
                tree, f"daily_activity_{date_var.get()}.csv"))
        export_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("Activity", "Book Title", "Member Name", "Date")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load today's data
        self.load_daily_activity(date.today().strftime('%Y-%m-%d'), tree)

    def load_daily_activity(self, date_str, tree):
        """Load daily activity data."""
        for item in tree.get_children():
            tree.delete(item)

        try:
            data = report_db.get_daily_activity_report(date_str)
            for row in data:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def create_fines_tab(self):
        """Create fines report tab."""
        fines_frame = ttk.Frame(self.notebook)
        self.notebook.add(fines_frame, text="💰 Fines")

        # Controls
        controls = ttk.Frame(fines_frame)
        controls.pack(fill=tk.X, pady=5)

        refresh_btn = ttk.Button(
            controls, text="Refresh",
            command=lambda: self.load_fines_data(tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            controls, text="Export CSV",
            command=lambda: self.export_treeview_to_csv(
                tree, "fines_report.csv"))
        export_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("ID", "Book Title", "Member Name", "Email",
                   "Due Date", "Return Date", "Fine", "Days Late")
        tree = ttk.Treeview(fines_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(fines_frame, orient=tk.VERTICAL,
                                  command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial data
        self.load_fines_data(tree)

    def load_fines_data(self, tree):
        """Load fines data."""
        for item in tree.get_children():
            tree.delete(item)

        data = report_db.get_fine_report()
        for row in data:
            # Format the row data
            formatted_row = list(row)
            formatted_row[6] = f"${row[6]:.2f}"  # Format fine amount
            formatted_row[7] = f"{int(row[7])}" if row[7] else "0"
            tree.insert("", tk.END, values=formatted_row)

    def export_treeview_to_csv(self, tree, filename):
        """Export treeview data to CSV file."""
        try:
            # Get desktop path for saving
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            filepath = os.path.join(desktop, filename)

            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write headers
                headers = [tree.heading(col)['text']
                           for col in tree['columns']]
                writer.writerow(headers)

                # Write data
                for item in tree.get_children():
                    values = tree.item(item)['values']
                    writer.writerow(values)

            messagebox.showinfo("Export Successful",
                                f"Data exported to {filepath}")

        except Exception as e:
            messagebox.showerror("Export Error",
                                 f"Failed to export data: {str(e)}")
