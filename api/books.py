from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_db
from repository.book_repository import BookRepository
from schemas.book_schema import BookCreate, BookResponse, PaginatedBookResponse
from services.auth_service import get_current_user, get_optional_current_user
from services.rate_limiter import rate_limit

router = APIRouter(prefix="/books", tags=["Books"])


def get_repository(db: AsyncIOMotorDatabase = Depends(get_db)):
    return BookRepository(db)


async def rate_limit_optional(
    request: Request,
    username: str | None = Depends(get_optional_current_user),
):
    """Анонімний → 2/хв, Авторизований → 10/хв."""
    await rate_limit(request, user_id=username)


async def get_rate_limited_user(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    """Тільки для авторизованих → 10/хв."""
    await rate_limit(request, user_id=current_user["username"])
    return current_user


@router.get("/", response_model=PaginatedBookResponse, response_model_by_alias=False)
async def get_all_books(
    skip: int = 0,
    limit: int = 10,
    repo: BookRepository = Depends(get_repository),
    _=Depends(rate_limit_optional),  # анонімний або авторизований
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
    _=Depends(rate_limit_optional),  # анонімний або авторизований
):
    book = await repo.get_by_id(book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.post("/", response_model=BookResponse, response_model_by_alias=False, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    repo: BookRepository = Depends(get_repository),
    _: dict = Depends(get_rate_limited_user),  # тільки авторизований
):
    return await repo.create(book_data=book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    repo: BookRepository = Depends(get_repository),
    _: dict = Depends(get_rate_limited_user),  # тільки авторизований
):
    if not await repo.delete(book_id=book_id):
        raise HTTPException(status_code=404, detail="Книгу не знайдено")