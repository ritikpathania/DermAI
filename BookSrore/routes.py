from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import books_collection
from models import Book

router = APIRouter()

def serialize_book(book):
    book["_id"] = str(book["_id"])
    return book

@router.post("/books")
def create_book(book: Book):
    result = books_collection.insert_one(book.dict())
    return {"_id": str(result.inserted_id)}

@router.get("/books")
def get_books():
    books = list(books_collection.find())
    return [serialize_book(book) for book in books]

@router.get("/books/{book_id}")
def get_book(book_id: str):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return serialize_book(book)

@router.put("/books/{book_id}")
def update_book(book_id: str, book: Book):
    result = books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": book.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated"}

@router.delete("/books/{book_id}")
def delete_book(book_id: str):
    result = books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
