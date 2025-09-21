from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory list to simulate a database for a book library
books = [
    {'book_id': 1, 'book_name': 'The Hitchhiker\'s Guide to the Galaxy', 'book_details': 'A hilarious science fiction comedy.'},
    {'book_id': 2, 'book_name': '1984', 'book_details': 'A dystopian social science fiction novel.'}
]
next_book_id = 3

## Get All Books

@app.route('/books', methods=['GET'])
def get_books():
    """Retrieves all books from the library."""
    return jsonify({'books': books})

## Get a Specific Book

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieves a single book by its ID."""
    book = next((book for book in books if book['book_id'] == book_id), None)
    if book:
        return jsonify({'book': book})
    return jsonify({'error': 'Book not found'}), 404

## Add a New Book

@app.route('/books', methods=['POST'])
def add_book():
    """Adds a new book to the library."""
    global next_book_id
    if not request.json or 'book_name' not in request.json or 'book_details' not in request.json:
        return jsonify({'error': 'Invalid request'}), 400

    new_book = {
        'book_id': next_book_id,
        'book_name': request.json['book_name'],
        'book_details': request.json['book_details']
    }
    books.append(new_book)
    next_book_id += 1
    return jsonify({'book': new_book}), 201

## Update an Existing Book

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Updates an existing book's details by its ID."""
    book = next((book for book in books if book['book_id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    if not request.json:
        return jsonify({'error': 'Invalid request'}), 400

    book['book_name'] = request.json.get('book_name', book['book_name'])
    book['book_details'] = request.json.get('book_details', book['book_details'])
    return jsonify({'book': book})

## Delete a Book

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Deletes a book from the library by its ID."""
    global books
    original_length = len(books)
    books = [book for book in books if book['book_id'] != book_id]
    
    if len(books) < original_length:
        return jsonify({'result': 'Book deleted'})
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)