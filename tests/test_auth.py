def test_register(client):
    res = client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    assert res.status_code == 201
    assert res.json()["username"] == "alice"


def test_register_duplicate(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    res = client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    assert res.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    res = client.post("/auth/login", json={"username": "alice", "password": "secret123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    res = client.post("/auth/login", json={"username": "alice", "password": "wrongpass"})
    assert res.status_code == 401


def test_refresh_token(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    login_res = client.post("/auth/login", json={"username": "alice", "password": "secret123"})
    refresh_token = login_res.json()["refresh_token"]

    res = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert "refresh_token" in res.json()


def test_refresh_with_access_token_fails(client):
    client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    login_res = client.post("/auth/login", json={"username": "alice", "password": "secret123"})
    access_token = login_res.json()["access_token"]

    res = client.post("/auth/refresh", json={"refresh_token": access_token})
    assert res.status_code == 401


def test_books_without_token(client):
    res = client.get("/books/")
    assert res.status_code == 200


def test_books_with_token(auth_client):
    res = auth_client.get("/books/")
    assert res.status_code == 200