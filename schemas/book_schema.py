from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List

class BookStatus(str, Enum):
    AVAILABLE = "наявні в бібліотеці"
    ISSUED = "видані комусь"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Назва книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    description: Optional[str] = Field(None, description="Опис книги")
    status: BookStatus = Field(default=BookStatus.AVAILABLE)
    year: int = Field(..., gt=0, description="Рік випуску")

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str
    model_config = {"from_attributes": True}

class PaginationInfo(BaseModel):
    limit: int
    cursor: Optional[str] = Field(None, description="Поточний курсор (ID книги)")
    next_cursor: Optional[str] = Field(None, description="Курсор для отримання наступної сторінки")
    count: int
    message: str

class PaginatedBookResponse(BaseModel):
    books: List[BookResponse]
    pagination: PaginationInfo