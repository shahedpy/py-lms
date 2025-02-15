""" gui > login.py """
import tkinter as tk
from tkinter import ttk, messagebox


class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
