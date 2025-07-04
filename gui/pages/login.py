""" gui > pages > login.py """
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import user_db


class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.load_logo()
        ttk.Label(
            self.frame,
            text="Library Management System",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 20))

        # Username field
        ttk.Label(
            self.frame, text="Username:", font=("Arial")).pack(anchor=tk.W)
        self.username_entry = ttk.Entry(
            self.frame, width=35, font=("Arial", 11))
        self.username_entry.pack(pady=5, ipady=5, anchor=tk.W)
        self.username_entry.focus()
        self.username_entry.bind(
            "<Return>", lambda event: self.password_entry.focus()
        )

        # Password field
        ttk.Label(
            self.frame, text="Password:", font=("Arial")).pack(anchor=tk.W)
        self.password_entry = ttk.Entry(
            self.frame, show="*", width=35, font=("Arial", 11))
        self.password_entry.pack(pady=5, ipady=5, anchor=tk.W)
        self.password_entry.bind(
            "<Return>", lambda event: self.check_login())

        self.login_button = ttk.Button(
            self.frame, text="Login", command=self.check_login)
        self.login_button.pack(pady=10)

    def load_logo(self):
        try:
            image = Image.open("assets/images/bubt_logo.png")
            image = image.resize((140, 140))
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_label = ttk.Label(self.frame, image=self.logo_image)
            self.logo_label.pack(pady=10)
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Error", "Username and password are required!"
            )
            return

        if self.authenticate_user(username, password):
            messagebox.showinfo("Success", "Login successful!")

    def authenticate_user(self, username, password):
        if user_db.authenticate_user(username, password):
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
