""" gui > book.py """
import tkinter as tk
from tkinter import ttk,  messagebox
from database.book import add_book, get_books


class BookPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(
            self.content, text="Books", font=("Arial", 14)
        )
        label.pack(pady=5)

        table_frame = ttk.Frame(self.content)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("ID", "Title", "Author", "Year")
        self.book_table = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=100)

        self.book_table.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.Frame(self.content)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0)
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=1, column=0, padx=5)

        ttk.Label(form_frame, text="Author:").grid(row=0, column=1)
        self.author_entry = ttk.Entry(form_frame)
        self.author_entry.grid(row=1, column=1, padx=5)

        ttk.Label(form_frame, text="Year:").grid(row=0, column=2)
        self.year_entry = ttk.Entry(form_frame)
        self.year_entry.grid(row=1, column=2, padx=5)

        button = ttk.Button(
            form_frame, text="Add Book", command=self.submit_book
        )
        button.grid(row=3, columnspan=3, pady=10)

        self.load_books()

    def load_books(self):
        books = get_books()
        self.book_table.delete(*self.book_table.get_children())

        for book in books:
            self.book_table.insert("", tk.END, values=book)

    def submit_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if title and author and year.isdigit():
            add_book(title, author, year)
            self.load_books()
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showerror("Error", "Invalid input!")
