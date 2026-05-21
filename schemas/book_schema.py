from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from typing import Optional

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
    id: UUID