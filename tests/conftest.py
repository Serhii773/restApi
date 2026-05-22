import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from main import app
from database import get_db

mock_client = AsyncMongoMockClient()
test_db = mock_client.test_library


@pytest.fixture(autouse=True)
async def setup_database():
    await test_db.books.drop()
    yield
    await test_db.books.drop()


@pytest.fixture
def client():
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()