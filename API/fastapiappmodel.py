from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic models for data validation and serialization
class Book(BaseModel):
    book_id: int
    book_name: str
    book_details: str

class BookCreate(BaseModel):
    book_name: str
    book_details: str

class BookUpdate(BaseModel):
    book_name: Optional[str] = None
    book_details: Optional[str] = None

# In-memory list to simulate a database
books_db = [
    {"book_id": 1, "book_name": "The Hitchhiker's Guide to the Galaxy", "book_details": "A hilarious science fiction comedy."},
    {"book_id": 2, "book_name": "1984", "book_details": "A dystopian social science fiction novel."}
]
next_book_id = 3

## GET All Books

@app.get("/books", response_model=List[Book])
def get_all_books():
    """Retrieves all books from the library."""
    return books_db

## GET a Specific Book

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """Retrieves a single book by its ID."""
    book = next((item for item in books_db if item["book_id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

## POST a New Book

@app.post("/books", response_model=Book, status_code=201)
def add_book(book: BookCreate):
    """Adds a new book to the library."""
    global next_book_id
    new_book = book.model_dump()
    new_book["book_id"] = next_book_id
    books_db.append(new_book)
    next_book_id += 1
    return new_book

## PUT to Update a Book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookUpdate):
    """Updates an existing book's details by its ID."""
    for index, book in enumerate(books_db):
        if book["book_id"] == book_id:
            if updated_book.book_name is not None:
                books_db[index]["book_name"] = updated_book.book_name
            if updated_book.book_details is not None:
                books_db[index]["book_details"] = updated_book.book_details
            return books_db[index]
    raise HTTPException(status_code=404, detail="Book not found")

## DELETE a Book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """Deletes a book from the library by its ID."""
    global books_db
    original_length = len(books_db)
    books_db = [book for book in books_db if book["book_id"] != book_id]
    if len(books_db) == original_length:
        raise HTTPException(status_code=404, detail="Book not found")
    return