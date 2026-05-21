from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from schemas.book_schema import BookCreate, BookResponse, BookStatus
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_all_books(
    book_status: Optional[BookStatus] = Query(None, description="Фільтр по статусу"),
    author: Optional[str] = Query(None, description="Фільтр по автору"),
    sort_by: Optional[str] = Query(None, description="Сортування ('title' або 'year')")
):
    status_str = book_status.value if book_status else None
    return await service.get_books(status=status_str, author=author, sort_by=sort_by)


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID):
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await service.create_book(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    await service.delete_book(book_id)