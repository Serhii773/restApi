from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_db
from repository.book_repository import BookRepository
from schemas.book_schema import BookCreate, BookResponse, PaginatedBookResponse
from services.auth_service import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])


def get_repository(db: AsyncIOMotorDatabase = Depends(get_db)):
    return BookRepository(db)


@router.post("/", response_model=BookResponse, response_model_by_alias=False, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    repo: BookRepository = Depends(get_repository),
    _: dict = Depends(get_current_user),
):
    return await repo.create(book_data=book)


@router.get("/", response_model=PaginatedBookResponse, response_model_by_alias=False)
async def get_all_books(
    skip: int = 0,
    limit: int = 10,
    repo: BookRepository = Depends(get_repository),
    _: dict = Depends(get_current_user),
):
    books = await repo.get_all(skip=skip, limit=limit)
    count = len(books)
    next_offset = skip + limit if count == limit else None

    return {
        "books": books,
        "pagination": {
            "limit": limit,
            "offset": skip,
            "next_offset": next_offset,
            "count": count,
            "message": f"You received books from {skip} to {skip + count}",
        },
    }


@router.get("/{book_id}", response_model=BookResponse, response_model_by_alias=False)
async def get_book(
    book_id: str,
    repo: BookRepository = Depends(get_repository),
    _: dict = Depends(get_current_user),
):
    book = await repo.get_by_id(book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    repo: BookRepository = Depends(get_repository),
    _: dict = Depends(get_current_user),
):
    if not await repo.delete(book_id=book_id):
        raise HTTPException(status_code=404, detail="Книгу не знайдено")