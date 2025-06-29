""" gui > pages > fine_management.py """
import tkinter as tk
from tkinter import ttk, messagebox
from database.transaction import transaction_db


class FineManagementPage:
    """Page for managing fine payments."""

    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding=10)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.load_unpaid_fines()

    def create_widgets(self):
        """Create the UI widgets."""
        # Title
        title_label = ttk.Label(
            self.content, text="💰 Fine Management",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Statistics frame
        stats_frame = ttk.Frame(self.content)
        stats_frame.pack(fill=tk.X, pady=10)

        # Statistics labels
        self.total_unpaid_label = ttk.Label(
            stats_frame, text="Total Unpaid: $0.00",
            font=("Arial", 12, "bold"), foreground="red"
        )
        self.total_unpaid_label.pack(side=tk.LEFT, padx=10)

        self.total_paid_label = ttk.Label(
            stats_frame, text="Total Paid: $0.00",
            font=("Arial", 12, "bold"), foreground="green"
        )
        self.total_paid_label.pack(side=tk.LEFT, padx=10)

        # Control buttons frame
        controls_frame = ttk.Frame(self.content)
        controls_frame.pack(fill=tk.X, pady=10)

        # Filter buttons
        ttk.Button(
            controls_frame, text="Show Unpaid Fines",
            command=self.load_unpaid_fines
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            controls_frame, text="Show Paid Fines",
            command=self.load_paid_fines
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            controls_frame, text="Show All Fines",
            command=self.load_all_fines
        ).pack(side=tk.LEFT, padx=5)

        # Action buttons
        ttk.Button(
            controls_frame, text="Mark as Paid",
            command=self.mark_selected_as_paid
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            controls_frame, text="Mark as Unpaid",
            command=self.mark_selected_as_unpaid
        ).pack(side=tk.RIGHT, padx=5)

        # Treeview for fines
        self.create_treeview()

        # Update statistics
        self.update_statistics()

    def create_treeview(self):
        """Create the treeview for displaying fines."""
        tree_frame = ttk.Frame(self.content)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Book Title", "Member Name", "Email", "Phone",
                   "Due Date", "Return Date", "Fine", "Status")

        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_unpaid_fines(self):
        """Load unpaid fines."""
        self.tree.delete(*self.tree.get_children())

        try:
            fines = transaction_db.get_unpaid_fines()
            for fine in fines:
                formatted_fine = list(fine)
                formatted_fine[7] = f"${fine[7]:.2f}"  # Format fine amount
                formatted_fine[8] = "Unpaid"  # Status
                self.tree.insert("", tk.END, values=formatted_fine)

            if not fines:
                self.tree.insert(
                    "", tk.END,
                    values=("", "No unpaid fines", "", "", "", "", "", "", ""))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load unpaid fines: {e}")

    def load_paid_fines(self):
        """Load paid fines."""
        self.tree.delete(*self.tree.get_children())

        try:
            fines = transaction_db.get_paid_fines()
            for fine in fines:
                formatted_fine = list(fine)
                formatted_fine[7] = f"${fine[7]:.2f}"  # Format fine amount
                formatted_fine[8] = "Paid"  # Status
                self.tree.insert("", tk.END, values=formatted_fine)

            if not fines:
                self.tree.insert(
                    "", tk.END,
                    values=("", "No paid fines", "", "", "", "", "", "", ""))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load paid fines: {e}")

    def load_all_fines(self):
        """Load all fines (both paid and unpaid)."""
        self.tree.delete(*self.tree.get_children())

        try:
            # Load unpaid fines
            unpaid_fines = transaction_db.get_unpaid_fines()
            for fine in unpaid_fines:
                formatted_fine = list(fine)
                formatted_fine[7] = f"${fine[7]:.2f}"
                formatted_fine[8] = "Unpaid"
                self.tree.insert("", tk.END, values=formatted_fine)

            # Load paid fines
            paid_fines = transaction_db.get_paid_fines()
            for fine in paid_fines:
                formatted_fine = list(fine)
                formatted_fine[7] = f"${fine[7]:.2f}"
                formatted_fine[8] = "Paid"
                self.tree.insert("", tk.END, values=formatted_fine)

            if not unpaid_fines and not paid_fines:
                self.tree.insert(
                    "", tk.END,
                    values=("", "No fines found", "", "", "", "", "", "", ""))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load fines: {e}")

    def mark_selected_as_paid(self):
        """Mark selected fines as paid."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select fine(s) to mark as paid.")
            return

        try:
            for item in selected_items:
                values = self.tree.item(item)['values']
                if values[0]:  # Check if there's a valid transaction ID
                    transaction_id = values[0]
                    transaction_db.mark_fine_as_paid(transaction_id)

            messagebox.showinfo(
                "Success", "Selected fine(s) marked as paid successfully.")
            self.load_unpaid_fines()  # Refresh the view
            self.update_statistics()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to mark fine as paid: {str(e)}")

    def mark_selected_as_unpaid(self):
        """Mark selected fines as unpaid."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Warning", "Please select fine(s) to mark as unpaid.")
            return

        try:
            for item in selected_items:
                values = self.tree.item(item)['values']
                if values[0]:  # Check if there's a valid transaction ID
                    transaction_id = values[0]
                    transaction_db.mark_fine_as_unpaid(transaction_id)

            messagebox.showinfo(
                "Success", "Selected fine(s) marked as unpaid successfully.")
            self.load_paid_fines()  # Refresh the view
            self.update_statistics()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to mark fine as unpaid: {str(e)}")

    def update_statistics(self):
        """Update the statistics labels."""
        try:
            total_unpaid = transaction_db.total_unpaid_fine()
            total_paid = transaction_db.total_paid_fine()

            self.total_unpaid_label.config(
                text=f"Total Unpaid: ${total_unpaid:.2f}")
            self.total_paid_label.config(
                text=f"Total Paid: ${total_paid:.2f}")

        except Exception as e:
            print(f"Error updating statistics: {e}")
