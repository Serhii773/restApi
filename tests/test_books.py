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
    created_books = []
    for book in books_to_create:
        res = client.post("/books/", json=book)
        created_books.append(res.json())

    created_books.sort(key=lambda x: x["id"])

    response = client.get("/books/?limit=2")
    assert response.status_code == 200
    data = response.json()

    assert len(data["books"]) == 2
    assert data["books"][0]["id"] == created_books[0]["id"]
    assert data["books"][1]["id"] == created_books[1]["id"]

    expected_cursor = created_books[1]["id"]
    assert data["pagination"]["next_cursor"] == expected_cursor

    response2 = client.get(f"/books/?cursor={expected_cursor}&limit=1")
    assert response2.status_code == 200
    data2 = response2.json()

    assert len(data2["books"]) == 1
    assert data2["books"][0]["id"] == created_books[2]["id"]

    assert data2["pagination"]["next_cursor"] == created_books[2]["id"]

    response3 = client.get(f"/books/?cursor={created_books[2]['id']}&limit=1")
    assert response3.status_code == 200
    data3 = response3.json()

    assert len(data3["books"]) == 0
    assert data3["pagination"]["next_cursor"] is None


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