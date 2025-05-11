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
- Login
    - Create Superuser
- Book
    - Book List
    - Add Book
    - Update Book
    - Delete Book
    - Search Book
- Member
    - Member List
- Issue
- Return
- Users
- Settings

## 📁 Project Structure
```
.
├── main.py
├── database/
│   ├── __init__.py
│   ├── models.py
│   ├── add_superuser.py
│   └── database.db
├── venv/
├── README.md
└── requirements.txt
```