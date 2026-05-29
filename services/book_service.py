from sqlalchemy.orm import Session
from repository.book_repository import BookRepository
from schemas.book_schema import BookCreate


class BookService:

    @staticmethod
    def get_all_books(db: Session, skip: int = 0, limit: int = 10):
        return BookRepository.get_all(db=db, skip=skip, limit=limit)

    @staticmethod
    def get_book_by_id(db: Session, book_id: str):
        return BookRepository.get_by_id(db=db, book_id=book_id)

    @staticmethod
    def create_book(db: Session, book_data: BookCreate):
        return BookRepository.create(db=db, book_data=book_data)

    @staticmethod
    def delete_book(db: Session, book_id: str):
        return BookRepository.delete(db=db, book_id=book_id)