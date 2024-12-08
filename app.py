from flask import Flask, request, jsonify
import sqlite3
from typing import List, Dict

app = Flask(__name__)

# to establish database connection
def db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn

def close_connection(conn: sqlite3.Connection):
    conn.commit()
    conn.close()

# add a new book 
@app.route('/add_book', methods=['POST'])
def add_book() -> str:
    data = request.json
    title = data['title']
    author = data['author']
    year_of_publication = data['year_of_publication']
    book_count = data['book_count']

    conn = db_connection()

    try:
        cursor = conn.cursor()
        
        # Check if the book already exists (same title and author)
        cursor.execute("SELECT * FROM books WHERE title = ? AND author = ?", (title, author))
        existing_book = cursor.fetchone()

        if existing_book:
            return jsonify({"error": "Book with the same title and author already exists"})
        
        # If book does not exist, insert new book
        cursor.execute("INSERT INTO books (title, author, year_of_publication, book_count) VALUES (?, ?, ?, ?)", (title, author, year_of_publication, book_count))
        close_connection(conn)
        
        return jsonify({"message": "Book added successfully"})

    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})
        
# get all books from the db
@app.route('/get_books', methods=['GET'])
def get_books() -> List[Dict]:
    conn = db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        close_connection(conn)

        books_list = []
        for book in books:
            books_list.append({
                'id': book['id'],
                'title': book['title'], 
                'author': book['author'], 
                'year_of_publication': book['year_of_publication'], 
                'book_count': book['book_count']
            })
        return jsonify(books_list)
    
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})

# update details of a book using ID
@app.route('/update_book/<int:id>', methods=["PUT"])
def update_book(id: int) -> str:
    data = request.json
    conn = db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
        book = cursor.fetchone()

        if not book:
            return jsonify({"error": "Book not found"})
        
        title = data.get('title', book['title'])
        author = data.get('author', book['author'])
        year_of_publication = data.get('year_of_publication', book['year_of_publication'])
        book_count = data.get('book_count', book['book_count'])

        cursor.execute("UPDATE books SET title = ?, author = ?, year_of_publication = ?, book_count = ? WHERE id = ?", (title, author, year_of_publication, book_count, id))
        close_connection(conn)

        return jsonify({"message": "Book updated successfully"})
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})

# delete a book based on ID
@app.route('/delete_book/<int:id>', methods=['DELETE'])
def delete_book(id: int) -> str:
    conn = db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = cursor.fetchone()

        if not book:
            return jsonify({"error": "Book not found"})

        cursor.execute('DELETE FROM books WHERE id = ?', (id,))
        close_connection(conn)

        return jsonify({"message": "Book deleted successfully"})
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})

# search for books by title or author
@app.route('/search_books', methods=["POST"])
def search_books() -> List[Dict]:
    data = request.json
    search_query = data.get('query', '')

    if not search_query:
        return jsonify({"error": "Please provide a search query"})
    
    conn = db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f'%{search_query}%', f'%{search_query}%'))
        books = cursor.fetchall()
        close_connection(conn)

        if books:
            books_list = []
            for book in books:
                books_list.append({
                    "id": book[0],
                    "title": book[1],
                    "author": book[2],
                    "year_of_publication": book[3],
                    "book_count": book[4]
                })
            return jsonify({"books": books_list})
        else:
            return jsonify({"message": "No books found matching the query"})
    
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})




# Add a new member
@app.route('/add_member', methods=['POST'])
def add_member() -> str:
    data = request.json
    name = data['name']
    email = data['email']

    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
        existing_member = cursor.fetchone()

        if existing_member:
            return jsonify({"error": "Email already exists"})
        
        # If email does not exist, insert new member
        cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        close_connection(conn)
        return jsonify({"message": "Member added successfully"})
    
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})

# Get all members
@app.route('/get_members', methods=['GET'])
def get_members() -> List[Dict]:
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        close_connection(conn)

        members_list = [{'id': member['id'], 'name': member['name'], 'email': member['email']} for member in members]
        return jsonify(members_list)
    
    except Exception as e:
        return jsonify({"error": str(e)})

# Update a member
@app.route('/update_member', methods=["PUT"])
def update_member() -> str:
    data = request.json
    email = data.get('email') 

    if not email:
        return jsonify({"error": "Email is required"})

    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
        member = cursor.fetchone()

        if not member:
            return jsonify({"error": "Member not found"})

        name = data.get('name', member['name'])

        cursor.execute("UPDATE members SET name = ? WHERE email = ?", (name, email))
        close_connection(conn)

        return jsonify({"message": "Member updated successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)})

# Delete a member
@app.route('/delete_member', methods=['DELETE'])
def delete_member() -> str:
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"})

    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Check if the member exists with the provided email
        cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
        member = cursor.fetchone()

        if not member:
            return jsonify({"error": "Member not found"})

        # Delete the member with the provided email
        cursor.execute("DELETE FROM members WHERE email = ?", (email,))
        close_connection(conn)

        return jsonify({"message": "Member deleted successfully"})
    
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})
    


# Search members by name or email
@app.route('/search_members', methods=["POST"])
def search_members() -> List[Dict]:
    data = request.json
    search_query = data.get('query', '')

    if not search_query:
        return jsonify({"error": "Please provide a search query"})

    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE name LIKE ? OR email LIKE ?", (f'%{search_query}%', f'%{search_query}%'))
        members = cursor.fetchall()
        close_connection(conn)

        if members:
            members_list = []
            for member in members:
                members_list.append({
                    "id": member['id'],
                    "name": member['name'],
                    "email": member['email']
                })
            return jsonify({"members": members_list})
        else:
            return jsonify({"message": "No members found matching the query"})
    
    except Exception as e:
        close_connection(conn)
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=8000)

