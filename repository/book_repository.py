import uuid
from typing import List, Dict, Optional
from models.book_store import books_db


class BookRepository:
    def get_all(self, skip=0, limit=10) -> List[Dict]:
        return books_db[skip:skip + limit]

    def get_by_id(self, book_id: str) -> Optional[Dict]:
        for book in books_db:
            if str(book["id"]) == book_id:
                return book
        return None

    def add(self, book_data: dict) -> dict:
        book_data["id"] = str(uuid.uuid4())
        books_db.append(book_data)
        return book_data

    def delete(self, book_id: str) -> bool:
        for i, book in enumerate(books_db):
            if str(book["id"]) == book_id:
                books_db.pop(i)
                return True
        return False