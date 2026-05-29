import uuid
from models.book_store import books_db
from typing import List, Dict, Optional

class BookRepository:
    async def get_all(self) -> List[Dict]:
        return books_db

    async def get_by_id(self, book_id: uuid.UUID) -> Optional[Dict]:
        for book in books_db:
            if book["id"] == book_id:
                return book
        return None

    async def add(self, book_data: dict) -> dict:
        book_data["id"] = uuid.uuid4()
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: uuid.UUID) -> None:
        global books_db
        books_db[:] = [book for book in books_db if book["id"] != book_id]