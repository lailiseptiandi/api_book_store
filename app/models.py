from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(Float)
    description = Column(Text)
    isbn = Column(String, unique=True)