def test_create_book(auth_client):
    res = auth_client.post("/books/", json={"title": "Тестова книга", "author": "Автор", "description": "Опис", "year": 2026})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Тестова книга"
    assert "id" in data


def test_get_all_books_pagination(auth_client):
    for i in range(1, 4):
        auth_client.post("/books/", json={"title": f"Книга {i}", "author": f"Автор {i}", "year": 2020 + i})

    res = auth_client.get("/books/?skip=0&limit=2")
    assert res.status_code == 200
    data = res.json()
    assert len(data["books"]) == 2
    assert data["pagination"]["next_offset"] == 2

    res = auth_client.get("/books/?skip=1&limit=1")
    data = res.json()
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Книга 2"


def test_get_book_by_id(auth_client):
    create_res = auth_client.post("/books/", json={"title": "Унікальна", "author": "Автор", "year": 2020})
    book_id = create_res.json()["id"]

    res = auth_client.get(f"/books/{book_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Унікальна"


def test_delete_book(auth_client):
    create_res = auth_client.post("/books/", json={"title": "На видалення", "author": "Автор", "year": 2010})
    book_id = create_res.json()["id"]

    assert auth_client.delete(f"/books/{book_id}").status_code == 204
    assert auth_client.get(f"/books/{book_id}").status_code == 404