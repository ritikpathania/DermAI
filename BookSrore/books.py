from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=200)
    rating: int = Field(gt=-1, lt=6)

BOOKS = []

@app.get("/")
def read_root():
    return BOOKS

@app.post("/books")
def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    count = 0

    for x in BOOKS:
        count += 1
        if x.id == book_id:
            BOOKS[count - 1] = book
            return BOOKS[count - 1]
        raise HTTPException(
            status_code=404,
            detail=f"ID: {book_id} Does not exist"
        )
    return None

@app.delete("/books/{book_id}")
def delete_book(book_id: UUID):
    count = 0

    for x in BOOKS:
        count += 1
        if x.id == book_id:
            del BOOKS[count - 1]
            return f"ID: {book_id} Deleted"
        raise HTTPException(
            status_code=404,
            detail=f"ID: {book_id} Does not exist"
        )
    return None