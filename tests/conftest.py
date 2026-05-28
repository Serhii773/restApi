import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from database import get_db
from main import app

mock_client = AsyncMongoMockClient()
test_db = mock_client.test_library


@pytest.fixture(autouse=True)
async def setup_database():
    await test_db.books.drop()
    await test_db.users.drop()
    yield
    await test_db.books.drop()
    await test_db.users.drop()


@pytest.fixture
def client():
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client):
    client.post("/auth/register", json={"username": "testuser", "password": "testpass123"})
    res = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    token = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client