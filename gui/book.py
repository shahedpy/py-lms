""" gui > book.py """
import tkinter as tk
from tkinter import ttk,  messagebox
from database.book import add_book, get_books, update_book


class BookPage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.content = ttk.Frame(self.parent_frame, padding="0")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.selected_book_id = None

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(
            self.content, text="Books", font=("Arial", 14)
        )
        label.pack(pady=5)

        table_frame = ttk.Frame(self.content)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("ID", "Title", "Author", "Year", "Price", "Created At")
        self.book_table = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=100)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.book_table.yview)
        self.book_table.configure(yscrollcommand=scrollbar.set)

        self.book_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_table.bind("<<TreeviewSelect>>", self.on_book_select)

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

        button_frame = ttk.Frame(self.content)
        button_frame.pack(pady=10)

        self.add_button = ttk.Button(
            button_frame, text="Add Book", command=self.submit_book
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = ttk.Button(
            button_frame, text="Update Book", command=self.update_selected_book
        )
        self.update_button.grid(row=0, column=1, padx=5)
        self.update_button["state"] = tk.DISABLED

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

    def on_book_select(self, event):
        selected = self.book_table.selection()
        if selected:
            book_data = self.book_table.item(selected[0], "values")
            self.selected_book_id = book_data[0]
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)

            self.title_entry.insert(0, book_data[1])
            self.author_entry.insert(0, book_data[2])
            self.year_entry.insert(0, book_data[3])

            self.update_button["state"] = tk.NORMAL
            self.add_button["state"] = tk.DISABLED

    def update_selected_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if title and author and year.isdigit():
            update_book(self.selected_book_id, title, author, year)
            self.book_table.selection_remove(self.book_table.selection())
            self.clear_form()
            self.load_books()
            messagebox.showinfo("Success", "Book updated successfully!")
        else:
            messagebox.showerror("Error", "Invalid input!")

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.selected_book_id = None
        self.update_button["state"] = tk.DISABLED
