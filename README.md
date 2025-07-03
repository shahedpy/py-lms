# Library Management System

A comprehensive desktop application for library management operations, developed using Python 3.13.3. This system provides a complete solution for managing library resources, member databases, and transaction workflows in an institutional environment.

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation and Setup](#installation-and-setup)
- [Usage Instructions](#usage-instructions)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Library Management System is designed to streamline library operations through an intuitive graphical user interface. The system supports comprehensive book cataloging, member management, transaction tracking, and detailed reporting capabilities. Built with Python's Tkinter framework, it provides a reliable and efficient solution for educational institutions and public libraries.

## System Requirements

- **Python Version**: 3.13.3 or higher
- **Operating System**: Windows, macOS, or Linux
- **Database**: SQLite (embedded)
- **Dependencies**: Listed in `requirements.txt`

## Installation and Setup

1. **Clone or download the project** to your local machine
2. **Install dependencies** (if any are specified in requirements.txt):
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the application** by running the main module:
   ```bash
   python main.py
   ```

### Administrative Setup

**Create a Superuser Account:**
```bash
python main.py createsuperuser
```

**Reset User Password:**
```bash
python main.py resetpassword
```

## Usage Instructions

1. Launch the application using `python main.py`
2. Login with your superuser credentials
3. Navigate through the interface to access different modules
4. Use the dashboard for real-time system overview

## Features

### Authentication and Security
- Secure user authentication system
- Role-based access control
- Password management and reset functionality
- Session management with automatic logout

### Book Management
- **Catalog Management**: Add, edit, and remove books from the library catalog
- **Inventory Control**: Track book availability and location
- **Search Functionality**: Advanced search and filtering capabilities
- **Book Details**: Comprehensive book information including ISBN, author, category, and publication details

### Member Management
- **Member Registration**: Register new library members with complete profile information
- **Profile Management**: Update member details and contact information
- **Member Status**: Track active and inactive memberships
- **History Tracking**: View member borrowing history and patterns

### Transaction Management
- **Book Issuing**: Process book checkouts with automated due date calculation
- **Return Processing**: Handle book returns with fine calculation for overdue items
- **Real-time Tracking**: Monitor currently issued books and their status
- **Fine Management**: Automated fine calculation and payment tracking

### Comprehensive Reporting System
- **Dashboard Analytics**: Real-time statistics and key performance indicators
- **Book Analytics**:
  - Most frequently issued titles
  - Unutilized inventory reports
  - Category-wise distribution analysis
- **Member Analytics**: Active member reports and borrowing behavior analysis
- **Transaction Reports**:
  - Overdue items with member contact details
  - Daily, weekly, and monthly activity logs
  - Issue and return transaction history
- **Financial Reports**: Fine collection summaries and payment tracking
- **Trend Analysis**: Monthly and yearly borrowing patterns
- **Data Export**: CSV export functionality for external analysis and record-keeping

### Notification System
- **Due Date Alerts**: Automated reminders for upcoming due dates
- **Fine Notifications**: Alert system for overdue items and associated penalties
- **System Messages**: User-friendly popup notifications for various system events


## Project Architecture

The application follows a modular architecture with clear separation of concerns:

```
Library Management System/
├── main.py                      # Application entry point and command-line interface
├── requirements.txt             # Project dependencies
├── README.md                   # Project documentation
│
├── assets/                     # Static resources
│   └── images/                # UI graphics and logos
│       ├── bubt_full_logo.png
│       └── bubt_logo.png
│
├── database/                   # Data layer and database operations
│   ├── __init__.py
│   ├── database.db            # SQLite database file
│   ├── db_connection.py       # Database connection management
│   ├── book.py                # Book entity operations
│   ├── user.py                # User authentication and management
│   ├── member.py              # Member entity operations
│   ├── transaction.py         # Transaction processing
│   ├── report.py              # Report generation and analytics
│   ├── createsuperuser.py     # Administrative user creation
│   └── resetpassword.py       # Password reset functionality
│
└── gui/                       # Presentation layer
    ├── __init__.py
    ├── controller.py          # Main application controller
    └── pages/                 # UI components and views
        ├── __init__.py
        ├── login.py           # Authentication interface
        ├── dashboard.py       # Main dashboard view
        ├── manage_books.py    # Book management interface
        ├── manage_members.py  # Member management interface
        ├── manage_users.py    # User administration interface
        ├── issue_book.py      # Book issuing interface
        ├── return_book.py     # Book return interface
        ├── member_details.py  # Member profile view
        ├── fine_management.py # Fine processing interface
        ├── change_password.py # Password change interface
        └── reports.py         # Reporting and analytics interface
```

### Architecture Components

- **Data Layer**: Handles all database operations, entity management, and data persistence
- **Business Logic**: Implements core library management rules and transaction processing
- **Presentation Layer**: Provides user interface components and user interaction handling
- **Controller**: Manages application flow and coordinates between data and presentation layers

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

Please ensure your code follows Python PEP 8 style guidelines and includes appropriate documentation.

## License

This project is developed for educational and institutional use.

---

**Version**: 1.0  
**Last Updated**: July 2025  
**Developed for**: Library Management Operations