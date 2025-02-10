from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        from_attributes = True
