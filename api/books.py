from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session

from schemas.book_schema import BookCreate, BookResponse, PaginatedBookResponse
from services.book_service import BookService
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return BookService.create_book(db=db, book_data=book)


@router.get("/", response_model=PaginatedBookResponse)
def get_all_books(cursor: Optional[str] = None, limit: int = 10, db: Session = Depends(get_db)):
    # 1. Отримуємо список книг за курсором
    books = BookService.get_all_books(db=db, cursor=cursor, limit=limit)

    # 2. Вираховуємо пагінацію
    count = len(books)

    # Якщо ми отримали максимальну кількість книг (limit), значить є наступна сторінка.
    # Курсором для неї стає ID останньої книги в поточному списку.
    next_cursor = books[-1].id if count == limit else None

    message = f"You received {count} books using cursor pagination"

    # 3. Повертаємо новий формат
    return {
        "books": books,
        "pagination": {
            "limit": limit,
            "cursor": cursor,
            "next_cursor": next_cursor,
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
    success = BookService.delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return