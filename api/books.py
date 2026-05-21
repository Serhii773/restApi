from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

# Додали імпорт PaginatedBookResponse
from schemas.book_schema import BookCreate, BookResponse, PaginatedBookResponse
from services.book_service import BookService
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Depends(get_db) автоматично відкриває сесію БД для цього запиту
    return BookService.create_book(db=db, book_data=book)


# Змінили response_model на PaginatedBookResponse
@router.get("/", response_model=PaginatedBookResponse)
def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Отримуємо список книг
    books = BookService.get_all_books(db=db, skip=skip, limit=limit)

    # Вираховуємо пагінацію
    count = len(books)
    next_offset = skip + limit if count == limit else None
    message = f"You received books from {skip} to {skip + count}"

    # Повертаємо новий формат
    return {
        "books": books,
        "pagination": {
            "limit": limit,
            "offset": skip,
            "next_offset": next_offset,
            "count": count,
            "message": message
        }
    }


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str, db: Session = Depends(get_db)):
    book = BookService.get_book_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str, db: Session = Depends(get_db)):
    # Зберігаємо результат видалення і перевіряємо його (щоб повертати 404)
    success = BookService.delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return