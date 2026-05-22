from fastapi import FastAPI
from api.books import router as books_router

app = FastAPI(
    title="Library API",
    description="API для управління бібліотекою (Lab 4 - FastAPI та MongoDB.)"
)

app.include_router(books_router)
