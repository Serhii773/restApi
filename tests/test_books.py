import uuid

def test_create_book(client):
    response = client.post(
        "/books/",
        json={
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "status": "наявні в бібліотеці"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "1984"
    assert "id" in response.json()

def test_get_all_books(client):
    client.post("/books/", json={"title": "Кобзар", "author": "Тарас Шевченко", "year": 1840})
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_all_books_filtering(client):
    client.post("/books/", json={"title": "Кобзар", "author": "Тарас Шевченко", "year": 1840})
    client.post("/books/", json={"title": "1984", "author": "George Orwell", "year": 1949})
    
    response = client.get("/books/?author=George Orwell")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "1984"

def test_get_book_by_id(client):
    create_resp = client.post("/books/", json={"title": "Кобзар", "author": "Тарас Шевченко", "year": 1840})
    book_id = create_resp.json()["id"]
    
    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Кобзар"

def test_get_book_not_found(client):
    random_id = str(uuid.uuid4())
    get_resp = client.get(f"/books/{random_id}")
    assert get_resp.status_code == 404

def test_delete_book(client):
    create_resp = client.post("/books/", json={"title": "Кобзар", "author": "Тарас Шевченко", "year": 1840})
    book_id = create_resp.json()["id"]

    del_resp = client.delete(f"/books/{book_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 404

def test_delete_book_idempotent(client):
    random_id = str(uuid.uuid4())
    del_resp = client.delete(f"/books/{random_id}")
    assert del_resp.status_code == 204