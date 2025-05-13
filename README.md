# 📚 Library Management System
A simple Library Management System built with Python 3.13.3. This application helps manage books, users, and transactions in a library environment.

## 🛠 Requirements
- Python: `3.13.3`
- No additional libraries required (unless specified in requirements.txt)

## ▶️ How to Run the Application
```bash
python main.py
```

## 👑 Create Superuser
```bash
python database/add_superuser.py
```

## Features
### 🔐 1. Login System
- Create Superuser
- Superuser Login
- Change Password
### 📚 2. Book Management
- Add new books
- Edit book info
- Delete Book
- View all books
- Search Books
### 👤 3. Member Management
- Register new members
- Update/delete member info
### 🔄 4. Book Issue and Return
- Issue a book to a member
- Track issue and return date
- Mark return and auto-calculate fine if overdue
- Show current borrowed books
### 📊 5. Reporting / Logs
- View issued books
- View overdue books
- Generate simple reports (total books, issued books, etc.)
### 🔔 6. Notifications (Basic)
- Simple popups for due return warning
- Fine alert while returning a book


## 📁 Project Structure
```
.
├── main.py
├── assets/images/
|   ├── bubt_full_logo.png
|   └── bubt_logo.png
├── database/
│   ├── __init__.py
│   ├── database.db
│   ├── add_superuser.py
│   ├── book.py
│   ├── member.py
│   └── transaction.py
├── gui/
│   ├── __init__.py
│   ├── controller.py
│   ├── login.py
│   ├── book.py
|   └── member.py
├── README.md
└── requirements.txt
```