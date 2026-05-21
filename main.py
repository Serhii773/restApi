import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import books
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "True":
        try:
            Base.metadata.create_all(bind=engine)
        except Exception:
            pass
    yield

app = FastAPI(
    title="Library API",
    description="API (Lab 3 - Cursor)",
    lifespan=lifespan
)

app.include_router(books.router)