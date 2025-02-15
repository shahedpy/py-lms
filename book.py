import tkinter as tk
from tkinter import ttk, messagebox
import database  # Assuming you have database functions to interact with a database


class BookManager:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Manage Books")
        self.window.geometry("600x400")

        # Book Form
        self.frame = ttk.Frame(self.window, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.book_id_entry = ttk.Entry(self.frame)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Title:").grid(row=1, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.frame)
        self.title_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Author:").grid(row=2, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(self.frame)
        self.author_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Year:").grid(row=3, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(self.frame)
        self.year_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="ISBN:").grid(row=4, column=0, padx=5, pady=5)
        self.isbn_entry = ttk.Entry(self.frame)
        self.isbn_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        self.add_button = ttk.Button(self.frame, text="Add Book", command=self.add_book)
        self.add_button.grid(row=5, column=0, pady=10)

        self.update_button = ttk.Button(self.frame, text="Update Book", command=self.update_book)
        self.update_button.grid(row=5, column=1, pady=10)

        self.delete_button = ttk.Button(self.frame, text="Delete Book", command=self.delete_book)
        self.delete_button.grid(row=6, column=0, pady=10)

        self.clear_button = ttk.Button(self.frame, text="Clear Fields", command=self.clear_fields)
        self.clear_button.grid(row=6, column=1, pady=10)

        # Book List
        self.book_list = ttk.Treeview(self.window, columns=("ID", "Title", "Author", "Year", "ISBN"), show="headings")
        self.book_list.heading("ID", text="ID")
        self.book_list.heading("Title", text="Title")
        self.book_list.heading("Author", text="Author")
        self.book_list.heading("Year", text="Year")
        self.book_list.heading("ISBN", text="ISBN")
        self.book_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.book_list.bind("<Double-1>", self.load_selected_book)
        self.load_books()

    def add_book(self):
        """Adds a book to the database."""
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()

        if not (title and author and year and isbn):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        database.add_book(title, author, year, isbn)
        self.load_books()
        self.clear_fields()
        messagebox.showinfo("Success", "Book added successfully!")

    def update_book(self):
        """Updates the selected book."""
        selected = self.book_list.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "No book selected!")
            return

        book_id = self.book_list.item(selected)["values"][0]
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()

        database.update_book(book_id, title, author, year, isbn)
        self.load_books()
        self.clear_fields()
        messagebox.showinfo("Success", "Book updated successfully!")

    def delete_book(self):
        """Deletes the selected book."""
        selected = self.book_list.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "No book selected!")
            return

        book_id = self.book_list.item(selected)["values"][0]
        database.delete_book(book_id)
        self.load_books()
        self.clear_fields()
        messagebox.showinfo("Success", "Book deleted successfully!")

    def load_selected_book(self, event):
        """Loads the selected book into the form."""
        selected = self.book_list.focus()
        if not selected:
            return

        values = self.book_list.item(selected)["values"]
        self.book_id_entry.delete(0, tk.END)
        self.book_id_entry.insert(0, values[0])
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])
        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, values[2])
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, values[3])
        self.isbn_entry.delete(0, tk.END)
        self.isbn_entry.insert(0, values[4])

    def load_books(self):
        """Loads books from the database."""
        self.book_list.delete(*self.book_list.get_children())
        books = database.get_books()
        for book in books:
            self.book_list.insert("", tk.END, values=book)

    def clear_fields(self):
        """Clears all input fields."""
        self.book_id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
