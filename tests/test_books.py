def test_create_book(client):
    response = client.post("/books/", json={
        "title": "Тестова книга",
        "author": "Тестовий автор",
        "description": "Опис книги",
        "year": 2026
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестова книга"
    assert "id" in data


def test_get_all_books_pagination(client):
    books_to_create = [
        {"title": "Книга 1", "author": "Автор 1", "year": 2021},
        {"title": "Книга 2", "author": "Автор 2", "year": 2022},
        {"title": "Книга 3", "author": "Автор 3", "year": 2023}
    ]
    for book in books_to_create:
        client.post("/books/", json=book)

    response = client.get("/books/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()

    assert "books" in data
    assert "pagination" in data
    assert len(data["books"]) == 2
    assert data["books"][0]["title"] == "Книга 1"
    assert data["books"][1]["title"] == "Книга 2"

    assert data["pagination"]["limit"] == 2
    assert data["pagination"]["offset"] == 0
    assert data["pagination"]["count"] == 2
    assert data["pagination"]["next_offset"] == 2

    response = client.get("/books/?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()

    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Книга 2"
    assert data["pagination"]["offset"] == 1
    assert data["pagination"]["limit"] == 1


def test_get_book_by_id(client):
    create_res = client.post("/books/", json={
        "title": "Унікальна книга",
        "author": "Автор",
        "year": 2020
    })
    book_id = create_res.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Унікальна книга"


def test_delete_book(client):
    create_res = client.post("/books/", json={
        "title": "Книга на видалення",
        "author": "Автор",
        "year": 2010
    })
    book_id = create_res.json()["id"]

    del_res = client.delete(f"/books/{book_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404