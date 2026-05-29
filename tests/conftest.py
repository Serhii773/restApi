import pytest
from fastapi.testclient import TestClient
from main import app
from models.book_store import books_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    books_db.clear()
    yield