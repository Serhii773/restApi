from fastapi import FastAPI
from api.books import router as books_router

app = FastAPI(
    title="Library API",
    description="API для бібліотеки (Лабораторна робота 1)"
)

app.include_router(books_router)