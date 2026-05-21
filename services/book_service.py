import uuid
from typing import Optional
from repository.book_repository import BookRepository
from schemas.book_schema import BookCreate

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(self, status: Optional[str] = None, author: Optional[str] = None, sort_by: Optional[str] = None):
        books = await self.repo.get_all()

        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if b["author"].lower() == author.lower()]

        if sort_by == "title":
            books.sort(key=lambda x: x["title"].lower())
        elif sort_by == "year":
            books.sort(key=lambda x: x["year"])
            
        return books

    async def get_book_by_id(self, book_id: uuid.UUID):
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book: BookCreate):
        return await self.repo.add(book.model_dump())

    async def delete_book(self, book_id: uuid.UUID):
        await self.repo.delete(book_id)