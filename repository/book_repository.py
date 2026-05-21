from sqlalchemy.orm import Session
from models.book_store import Book
from schemas.book_schema import BookCreate


class BookRepository:

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10):
        """
        Отримання списку книг з Limit-Offset пагінацією.
        skip (offset) - скільки записів пропустити з початку.
        limit - максимальна кількість записів, які треба повернути.
        """
        return db.query(Book).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, book_id: str):
        # Шукаємо книгу за її id в базі даних
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def create(db: Session, book_data: BookCreate):
        # Створюємо об'єкт моделі SQLAlchemy (розпаковуємо дані зі схеми)
        db_book = Book(**book_data.model_dump())
        db.add(db_book)  # Додаємо в сесію
        db.commit()  # Зберігаємо (комітимо) в базу
        db.refresh(db_book)  # Оновлюємо об'єкт, щоб отримати згенерований id
        return db_book

    @staticmethod
    def delete(db: Session, book_id: str):
        # Знаходимо книгу, і якщо вона є - видаляємо
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False