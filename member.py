import sqlite3

# Database connection
DB_NAME = "library.db"

def connect():
    """Connect to the database and create the members table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_member(name, email, phone, address):
    """Add a new member to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (name, email, phone, address) VALUES (?, ?, ?, ?)", 
                   (name, email, phone, address))
    conn.commit()
    conn.close()

def get_members():
    """Retrieve all members from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return members

def update_member(member_id, name, email, phone, address):
    """Update an existing member's details."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?
    """, (name, email, phone, address, member_id))
    conn.commit()
    conn.close()

def delete_member(member_id):
    """Delete a member from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()

def search_members(name="", email="", phone=""):
    """Search for members based on given criteria."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT * FROM members WHERE name LIKE ? AND email LIKE ? AND phone LIKE ?"
    cursor.execute(query, ('%' + name + '%', '%' + email + '%', '%' + phone + '%'))
    members = cursor.fetchall()
    conn.close()
    return members

# Ensure the database is created when the module is imported
connect()
