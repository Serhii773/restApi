from sqlalchemy.orm import Session
from typing import Optional
from models.book_store import Book
from schemas.book_schema import BookCreate


class BookRepository:

    @staticmethod
    def get_all(db: Session, cursor: Optional[str] = None, limit: int = 10):
        query = db.query(Book).order_by(Book.id)

        if cursor:
            query = query.filter(Book.id > cursor)

        return query.limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, book_id: str):
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def create(db: Session, book_data: BookCreate):
        db_book = Book(**book_data.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete(db: Session, book_id: str):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False