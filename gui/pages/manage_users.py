""" gui > pages > manage_users.py """
import tkinter as tk
from tkinter import ttk, messagebox
from database import user_db


class ManageUserPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.selected_user_id = None
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self.content, text="👥 Manage Users", font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Search frame
        search_frame = ttk.Frame(self.content)
        search_frame.pack(pady=5)
        ttk.Label(
            search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(
            search_frame, text="Search", command=self.search_users)
        search_button.pack(side=tk.LEFT, padx=5)
        reset_button = ttk.Button(
            search_frame, text="Reset", command=self.reset_search)
        reset_button.pack(side=tk.LEFT, padx=5)

        # Table frame
        table_frame = ttk.Frame(self.content)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("ID", "Username", "Active", "Superuser")
        self.user_table = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.user_table.heading(col, text=col)
            if col == "ID":
                self.user_table.column(col, width=50)
            elif col == "Username":
                self.user_table.column(col, width=200)
            else:
                self.user_table.column(col, width=100)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.user_table.yview
        )
        self.user_table.configure(yscrollcommand=scrollbar.set)

        self.user_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.user_table.bind("<<TreeviewSelect>>", self.on_user_select)

        # Form frame
        form_frame = ttk.Frame(self.content)
        form_frame.pack(pady=10)

        # Username field
        ttk.Label(form_frame, text="Username:").grid(
            row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(form_frame, width=20)
        self.username_entry.grid(row=1, column=0, padx=5)

        # Password field
        ttk.Label(form_frame, text="Password:").grid(
            row=0, column=1, sticky="w")
        self.password_entry = ttk.Entry(form_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5)

        # Active checkbox
        self.is_active_var = tk.BooleanVar(value=True)
        self.active_checkbox = ttk.Checkbutton(
            form_frame, text="Active", variable=self.is_active_var
        )
        self.active_checkbox.grid(row=1, column=2, padx=5)

        # Superuser checkbox
        self.is_superuser_var = tk.BooleanVar()
        self.superuser_checkbox = ttk.Checkbutton(
            form_frame, text="Superuser", variable=self.is_superuser_var
        )
        self.superuser_checkbox.grid(row=1, column=3, padx=5)

        # Button frame
        button_frame = ttk.Frame(self.content)
        button_frame.pack(pady=10)

        self.add_button = ttk.Button(
            button_frame, text="Add User", command=self.add_user
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = ttk.Button(
            button_frame, text="Update User", command=self.update_selected_user
        )
        self.update_button.grid(row=0, column=1, padx=5)
        self.update_button["state"] = tk.DISABLED

        self.reset_password_button = ttk.Button(
            button_frame, text="Reset Password", command=self.reset_password
        )
        self.reset_password_button.grid(row=0, column=2, padx=5)
        self.reset_password_button["state"] = tk.DISABLED

        self.delete_button = ttk.Button(
            button_frame, text="Delete User", command=self.delete_selected_user
        )
        self.delete_button.grid(row=0, column=3, padx=5)
        self.delete_button["state"] = tk.DISABLED

        self.load_users()

    def load_users(self):
        """Load all users into the table"""
        users = user_db.get_users()
        self.user_table.delete(*self.user_table.get_children())

        for user in users:
            user_id, username, is_active, is_superuser = user
            active_text = "Yes" if is_active else "No"
            superuser_text = "Yes" if is_superuser else "No"
            self.user_table.insert(
                "", tk.END,
                values=(user_id, username, active_text, superuser_text)
            )

    def search_users(self):
        """Search users by username"""
        keyword = self.search_entry.get().strip()
        if keyword:
            users = user_db.search_users(keyword)
            self.user_table.delete(*self.user_table.get_children())
            for user in users:
                user_id, username, is_active, is_superuser = user
                active_text = "Yes" if is_active else "No"
                superuser_text = "Yes" if is_superuser else "No"
                self.user_table.insert(
                    "", tk.END,
                    values=(user_id, username, active_text, superuser_text)
                )
        else:
            messagebox.showwarning(
                "Input Needed", "Please enter a keyword to search."
            )

    def reset_search(self):
        """Reset search and reload all users"""
        self.search_entry.delete(0, tk.END)
        self.load_users()

    def add_user(self):
        """Add a new user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        is_superuser = self.is_superuser_var.get()

        if not username or not password:
            messagebox.showerror(
                "Error", "Username and password are required!")
            return

        if len(password) < 6:
            messagebox.showerror(
                "Error", "Password must be at least 6 characters long!")
            return

        success = user_db.add_user(username, password, is_superuser)
        if success:
            self.clear_form()
            self.load_users()
            messagebox.showinfo("Success", "User added successfully!")
        else:
            messagebox.showerror(
                "Error", "Failed to add user. Username might already exist.")

    def on_user_select(self, event):
        """Handle user selection from table"""
        selected = self.user_table.selection()
        if selected:
            user_data = self.user_table.item(selected[0], "values")
            self.selected_user_id = user_data[0]

            # Fill form with selected user data
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, user_data[1])
            self.username_entry.configure(state='readonly')

            # Clear password field (for security)
            self.password_entry.delete(0, tk.END)
            self.password_entry.configure(state='disabled')

            # Set checkboxes
            self.is_active_var.set(user_data[2] == "Yes")
            self.is_superuser_var.set(user_data[3] == "Yes")

            # Enable/disable buttons
            self.update_button["state"] = tk.NORMAL
            self.reset_password_button["state"] = tk.NORMAL
            self.delete_button["state"] = tk.NORMAL
            self.add_button["state"] = tk.DISABLED

    def update_selected_user(self):
        """Update the selected user's status and role"""
        if not self.selected_user_id:
            return

        is_active = self.is_active_var.get()
        is_superuser = self.is_superuser_var.get()

        # Update user status and role
        status_success = user_db.update_user_status(
            self.selected_user_id, is_active)
        role_success = user_db.update_user_role(
            self.selected_user_id, is_superuser)

        if status_success and role_success:
            self.clear_form()
            self.load_users()
            messagebox.showinfo("Success", "User updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update user!")

    def reset_password(self):
        """Reset password for selected user"""
        if not self.selected_user_id:
            return

        # Create a dialog to get new password
        password_dialog = tk.Toplevel(self.content)
        password_dialog.title("Reset Password")
        password_dialog.geometry("300x150")
        password_dialog.resizable(False, False)
        password_dialog.grab_set()

        ttk.Label(password_dialog, text="New Password:").pack(pady=10)
        new_password_entry = ttk.Entry(password_dialog, show="*", width=30)
        new_password_entry.pack(pady=5)

        ttk.Label(password_dialog, text="Confirm Password:").pack(pady=(10, 0))
        confirm_password_entry = ttk.Entry(password_dialog, show="*", width=30)
        confirm_password_entry.pack(pady=5)

        def confirm_reset():
            new_password = new_password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()

            if not new_password or not confirm_password:
                messagebox.showerror("Error", "Both fields are required!")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            if len(new_password) < 6:
                messagebox.showerror(
                    "Error", "Password must be at least 6 characters long!")
                return

            # Get username for reset
            selected = self.user_table.selection()
            if selected:
                user_data = self.user_table.item(selected[0], "values")
                username = user_data[1]

                success, message = user_db.reset_password(
                    username, new_password)
                if success:
                    password_dialog.destroy()
                    messagebox.showinfo(
                        "Success", "Password reset successfully!")
                else:
                    messagebox.showerror(
                        "Error", f"Failed to reset password: {message}")

        button_frame = ttk.Frame(password_dialog)
        button_frame.pack(pady=10)

        reset_btn = ttk.Button(
            button_frame, text="Reset", command=confirm_reset)
        reset_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(
            button_frame, text="Cancel", command=password_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        new_password_entry.focus()

    def delete_selected_user(self):
        """Delete the selected user"""
        if not self.selected_user_id:
            return

        selected = self.user_table.selection()
        if selected:
            user_data = self.user_table.item(selected[0], "values")
            username = user_data[1]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the user '{username}'?\n\n"
                "This action cannot be undone!"
            )
            if confirm:
                success = user_db.delete_user(self.selected_user_id)
                if success:
                    self.clear_form()
                    self.load_users()
                    messagebox.showinfo(
                        "Success", "User deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete user!")

    def clear_form(self):
        """Clear the form and reset buttons"""
        self.username_entry.configure(state='normal')
        self.username_entry.delete(0, tk.END)

        self.password_entry.configure(state='normal')
        self.password_entry.delete(0, tk.END)

        self.is_active_var.set(True)
        self.is_superuser_var.set(False)

        self.selected_user_id = None
        self.add_button["state"] = tk.NORMAL
        self.update_button["state"] = tk.DISABLED
        self.reset_password_button["state"] = tk.DISABLED
        self.delete_button["state"] = tk.DISABLED
