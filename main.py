import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import books
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Створюємо таблиці в PostgreSQL ТІЛЬКИ якщо це НЕ тести
    if os.getenv("TESTING") != "True":
        try:
            Base.metadata.create_all(bind=engine)
        except Exception:
            pass
    yield

app = FastAPI(
    title="Library API",
    description="API для управління бібліотекою (Lab 2 - PostgreSQL & Docker)",
    lifespan=lifespan
)

app.include_router(books.router)