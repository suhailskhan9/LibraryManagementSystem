# Library Management System

This is a simple **Library Management System** built using Flask and SQLite.

## How to Run the Project

- Python installed.
- SQLite3 installed (SQLite is used as the database for this application).
- No third-party libraries have been used in this project

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/library-management-system.git

2. Navigate to the project directory:
   ```bash
   cd library-management-system
   
3. Create the database by running the following commands in your Python shell or script:
   ```bash
   import sqlite3

   # Create and connect to the database
   conn = sqlite3.connect('library.db')
    
   # Create tables for books and members
   conn.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year_of_publication INTEGER NOT NULL,
        book_count INTEGER NOT NULL
   )''')
    
   conn.execute('''CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
   )''')
    
   conn.close()
   
4. Once the database and tables are set up, run the Flask application:
    ```bash
     py app.py
     ```



# Endpoints
### 1. `/add_book` [POST]
- Adds a new book to the library.
- **Request Body**: JSON object with `title`, `author`, `year_of_publication`, and `book_count`.
- **Response**: Success or error message.

### 2. `/get_books` [GET]
- Retrieves all books in the library.
- **Response**: List of books with `id`, `title`, `author`, `year_of_publication`, and `book_count`.

### 3. `/update_book/<id>` [PUT]
- Updates details of a book using its ID.
- **Request Body**: JSON object with `title`, `author`, `year_of_publication`, and `book_count` (optional; fields to update).
- **Response**: Success or error message.

### 4. `/delete_book/<id>` [DELETE]
- Deletes a book by its ID.
- **Response**: Success or error message.

### 5. `/search_books` [POST]
- Searches for books by title or author.
- **Request Body**: JSON object with a `query` string.
- **Response**: List of books matching the search query.

### 6. `/add_member` [POST]
- Adds a new member to the library.
- **Request Body**: JSON object with `name` and `email`.
- **Response**: Success or error message.

### 7. `/get_members` [GET]
- Retrieves all members of the library.
- **Response**: List of members with `id`, `name`, and `email`.

### 8. `/update_member` [PUT]
- Updates details of a member.
- **Request Body**: JSON object with `name` and `email` (at least `email` is required).
- **Response**: Success or error message.

### 9. `/delete_member` [DELETE]
- Deletes a member by their email.
- **Request Body**: JSON object with `email`.
- **Response**: Success or error message.

### 10. `/search_members` [POST]
- Searches for members by name or email.
- **Request Body**: JSON object with a `query` string.
- **Response**: List of members matching the search query.
