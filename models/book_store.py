from sqlalchemy import Column, String, Integer
from database import Base
import uuid

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="наявні в бібліотеці")
    year = Column(Integer, nullable=False)