# Use Case Diagram - Library Management System

## Use Case Diagram

```
                    Library Management System - Use Case Diagram
                                        
                                 ┌─────────────────────────┐
                                 │   Library Management    │
                                 │        System           │
                                 └─────────────────────────┘
                                            │
           ┌────────────────────────────────┼─────────────────────────────────┐
           │                                │                                 │
           │                                │                                 │
    ┌──────▼──────┐                         │                      ┌──────▼──────┐
    │             │          Authentication │                      │             │
    │ Librarian/  │◄────────────────────────┼───────-─────────────►│   Member    │
    │ Admin User  │                         │                      │   (Read-    │
    │             │                         │                      │   Only)     │
    └─────────────┘                         │                      └─────────────┘
           │                                 │                             │
           │                                 │                             │
           │              System Use Cases   │                             │
           │                                 │                             │
    ┌──────▼──────────────────────────────────▼─────────────────────────────▼──────┐
    │                                                                              │
    │  Authentication & User Management:                                           │
    │  ○ Login to System                                                           │
    │  ○ Change Password                                                           │
    │  ○ Logout                                                                    │
    │  ○ Create Superuser (Admin)                                                  │
    │  ○ Manage Users (Admin only)                                                 │
    │  ○ Reset Password (Admin)                                                    │
    │                                                                              │
    │  Book Management:                                                            │
    │  ○ Add New Book                                                              │
    │  ○ Edit Book Information                                                     │
    │  ○ Delete Book                                                               │
    │  ○ Search Books                                                              │
    │  ○ View Book Details                                                         │
    │  ○ View Book Availability                                                    │
    │                                                                              │
    │  Member Management:                                                          │
    │  ○ Register New Member                                                       │
    │  ○ Edit Member Information                                                   │
    │  ○ Delete Member                                                             │
    │  ○ Search Members                                                            │
    │  ○ View Member Details                                                       │
    │  ○ View Member History                                                       │
    │  ○ Activate/Deactivate Member                                                │
    │                                                                              │
    │  Transaction Management:                                                     │
    │  ○ Issue Book to Member                                                      │
    │  ○ Return Book from Member                                                   │
    │  ○ Calculate Due Date                                                        │
    │  ○ View Transaction History                                                  │
    │  ○ Track Book Status                                                         │
    │                                                                              │
    │  Fine Management:                                                            │
    │  ○ Calculate Overdue Fines                                                   │
    │  ○ Process Fine Payment                                                      │
    │  ○ View Fine History                                                         │
    │  ○ Generate Fine Reports                                                     │
    │  ○ Send Overdue Notifications                                                │
    │                                                                              │
    │  Reports & Analytics:                                                        │
    │  ○ View Dashboard Statistics                                                 │
    │  ○ Generate Book Reports                                                     │
    │  ○ Generate Member Reports                                                   │
    │  ○ Generate Transaction Reports                                              │
    │  ○ Generate Financial Reports                                                │
    │  ○ Export Reports to CSV                                                     │
    │  ○ View System Analytics                                                     │
    │                                                                              │
    └──────────────────────────────────────────────────────────────────────────────┘

    Actors:
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │  👤 Librarian/Admin User:                                                   │
    │     • Full access to all system functionalities                             │
    │     • Can manage books, members, transactions, and users                    │
    │     • Can generate reports and view analytics                               │
    │     • Can process fines and manage system settings                          │
    │                                                                             │
    │  👥 Member (Read-Only):                                                     │
    │     • Limited access for viewing purposes only                              │
    │     • Can view their borrowing history                                      │
    │     • Can check book availability                                           │
    │     • Cannot perform administrative functions                               │
    │                                                                             │
    │  🖥️  System:                                                                │
    │     • Automated fine calculation                                           │
    │     • Due date notifications                                               │
    │     • Inventory management                                                 │
    │     • Data validation and integrity                                        │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘

    Key Relationships:
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │  • Librarian «extends» Member capabilities                                  │
    │  • Issue Book «includes» Check Book Availability                            │
    │  • Return Book «includes» Calculate Fine                                    │
    │  • All operations «require» Authentication                                  │
    │  • Report Generation «uses» Transaction Data                                │
    │  • Fine Management «depends on» Transaction Records                         │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
```

## Use Case Descriptions

### Primary Use Cases

#### Authentication & Security
- **Login**: Users authenticate with username/password to access the system
- **Change Password**: Users can update their passwords for security
- **User Management**: Admin can create, modify, and manage user accounts

#### Core Library Operations
- **Book Management**: Complete CRUD operations for library inventory
- **Member Management**: Registration and maintenance of library member records
- **Transaction Processing**: Handle book borrowing and returning workflows

#### Advanced Features
- **Fine Management**: Automated calculation and processing of overdue penalties
- **Reporting System**: Comprehensive analytics and data export capabilities
- **Dashboard Analytics**: Real-time system statistics and performance metrics

### System Boundaries
The system operates as a desktop application with local SQLite database storage, providing comprehensive library management capabilities for educational institutions and public libraries.