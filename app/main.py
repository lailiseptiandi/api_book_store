from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore API",
    description="API for managing bookstore inventory",
    version="1.0.0",
    openapi_tags=[{
        "name": "books",
        "description": "Operations with books"
    }]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=schemas.Book, tags=["books"])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book with the following information:
    - **title**: Title of the book
    - **author**: Author of the book
    - **price**: Price of the book
    - **description**: Optional description
    - **isbn**: Unique ISBN number
    """
    db_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="ISBN already registered")
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[schemas.Book], tags=["books"])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all books with pagination support:
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=schemas.Book, tags=["books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a specific book by its ID
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=schemas.Book, tags=["books"])
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Update a book's information
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", tags=["books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted"}