import pytest
from main import create_app
from models.book_store import books_db


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    books_db.clear()
    yield app.test_client()
    books_db.clear()