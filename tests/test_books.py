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
    # Створюємо 3 книги для перевірки пагінації
    books_to_create = [
        {"title": "Книга 1", "author": "Автор 1", "year": 2021},
        {"title": "Книга 2", "author": "Автор 2", "year": 2022},
        {"title": "Книга 3", "author": "Автор 3", "year": 2023}
    ]
    for book in books_to_create:
        client.post("/books/", json=book)

    # Тестуємо limit=2 (має повернути тільки перші 2 книги всередині ключа "books")
    response = client.get("/books/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()

    # Перевіряємо нову структуру відповіді з метаданими
    assert "books" in data
    assert "pagination" in data
    assert len(data["books"]) == 2
    assert data["books"][0]["title"] == "Книга 1"
    assert data["books"][1]["title"] == "Книга 2"

    # Перевіряємо правильність заповнення блоку пагінації
    assert data["pagination"]["limit"] == 2
    assert data["pagination"]["offset"] == 0
    assert data["pagination"]["count"] == 2
    assert data["pagination"]["next_offset"] == 2

    # Тестуємо skip=1 та limit=1 (має пропустити першу і повернути тільки другу)
    response = client.get("/books/?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()

    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Книга 2"
    assert data["pagination"]["offset"] == 1
    assert data["pagination"]["limit"] == 1


def test_get_book_by_id(client):
    # Спочатку створюємо книгу
    create_res = client.post("/books/", json={
        "title": "Унікальна книга",
        "author": "Автор",
        "year": 2020
    })
    book_id = create_res.json()["id"]

    # Пробуємо її дістати за id
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

    # Видаляємо
    del_res = client.delete(f"/books/{book_id}")
    assert del_res.status_code == 204

    # Перевіряємо, що її більше немає
    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404