from motor.motor_asyncio import AsyncIOMotorDatabase
from repository.book_repository import BookRepository
from schemas.book_schema import BookCreate

class BookService:

    @staticmethod
    async def get_all_books(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 10):
        repo = BookRepository(db)
        return await repo.get_all(skip=skip, limit=limit)

    @staticmethod
    async def get_book_by_id(db: AsyncIOMotorDatabase, book_id: str):
        repo = BookRepository(db)
        return await repo.get_by_id(book_id=book_id)

    @staticmethod
    async def create_book(db: AsyncIOMotorDatabase, book_data: BookCreate):
        repo = BookRepository(db)
        return await repo.create(book_data=book_data)

    @staticmethod
    async def delete_book(db: AsyncIOMotorDatabase, book_id: str):
        repo = BookRepository(db)
        return await repo.delete(book_id=book_id)