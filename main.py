from fastapi import FastAPI

from api.auth import router as auth_router
from api.books import router as books_router

app = FastAPI(
    title="Library API",
    description="API для управління бібліотекою (Lab 6 - JWT Auth)",
)

app.include_router(auth_router)
app.include_router(books_router)