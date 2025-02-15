import sqlite3

# Database connection
DB_NAME = "library.db"

def connect():
    """Connect to the database and create tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            isbn TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def add_book(title, author, year, isbn):
    """Add a new book to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", 
                   (title, author, year, isbn))
    conn.commit()
    conn.close()

def get_books():
    """Retrieve all books from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, title, author, year, isbn):
    """Update an existing book in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?
    """, (title, author, year, isbn, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    """Delete a book from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def search_books(title="", author="", year="", isbn=""):
    """Search for books based on given criteria."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND year LIKE ? AND isbn LIKE ?"
    cursor.execute(query, ('%' + title + '%', '%' + author + '%', '%' + year + '%', '%' + isbn + '%'))
    books = cursor.fetchall()
    conn.close()
    return books

# Ensure the database is created when the module is imported
connect()
