""" gui > login.py """
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_logo()
        ttk.Label(self.frame, text="Library Management System", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(self.frame, text="Username:").pack()
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password:").pack()
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.frame, text="Login", command=self.check_login)
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
        messagebox.showinfo("Developing", "Coming soon!")
