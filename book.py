import tkinter as tk
from tkinter import ttk


class BookManager:
    def __init__(self, book):
        self.window = tk.Tk()
        self.window.title('Manage Book')
        self.window.geometry('400x200')

        # Book Form
        self.frame = ttk.Frame(self.window, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5) # noqa
        self.book_id_entry = ttk.Entry(self.frame)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Title:").grid(row=1, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.frame)
        self.title_entry.grid(row=1, column=1, padx=5, pady=5)

    def add_book(self):
        title = self.title_entry.get()

        
