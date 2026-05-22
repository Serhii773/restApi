from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.book_schema import BookCreate, BookResponse, PaginatedBookResponse
from repository.book_repository import BookRepository
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


def get_repository(db: AsyncIOMotorDatabase = Depends(get_db)):
    return BookRepository(db)


@router.post("/", response_model=BookResponse, response_model_by_alias=False, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, repo: BookRepository = Depends(get_repository)):
    return await repo.create(book_data=book)


@router.get("/", response_model=PaginatedBookResponse, response_model_by_alias=False)
async def get_all_books(skip: int = 0, limit: int = 10, repo: BookRepository = Depends(get_repository)):
    books = await repo.get_all(skip=skip, limit=limit)

    count = len(books)
    next_offset = skip + limit if count == limit else None
    message = f"You received books from {skip} to {skip + count}"

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


@router.get("/{book_id}", response_model=BookResponse, response_model_by_alias=False)
async def get_book(book_id: str, repo: BookRepository = Depends(get_repository)):
    book = await repo.get_by_id(book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, repo: BookRepository = Depends(get_repository)):
    success = await repo.delete(book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return