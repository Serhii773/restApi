def test_create_book(client):
    response = client.post('/books', json={
        'title': 'Кобзар',
        'author': 'Тарас Шевченко',
        'year': 1840
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Кобзар'
    assert 'id' in data


def test_get_all_books(client):
    client.post('/books', json={'title': 'Книга 1', 'author': 'Автор 1', 'year': 2021})
    client.post('/books', json={'title': 'Книга 2', 'author': 'Автор 2', 'year': 2022})

    response = client.get('/books')
    assert response.status_code == 200
    data = response.get_json()
    assert 'books' in data
    assert len(data['books']) == 2


def test_get_all_books_pagination(client):
    for i in range(3):
        client.post('/books', json={'title': f'Книга {i}', 'author': 'Автор', 'year': 2020 + i})

    response = client.get('/books?skip=0&limit=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['books']) == 2
    assert data['pagination']['next_offset'] == 2

    response = client.get('/books?skip=2&limit=2')
    data = response.get_json()
    assert len(data['books']) == 1
    assert data['pagination']['next_offset'] is None


def test_get_book_by_id(client):
    create_res = client.post('/books', json={
        'title': 'Унікальна книга',
        'author': 'Автор',
        'year': 2020
    })
    book_id = create_res.get_json()['id']

    response = client.get(f'/books/{book_id}')
    assert response.status_code == 200
    assert response.get_json()['title'] == 'Унікальна книга'


def test_get_book_not_found(client):
    response = client.get('/books/999')
    assert response.status_code == 404


def test_delete_book(client):
    create_res = client.post('/books', json={
        'title': 'Книга на видалення',
        'author': 'Автор',
        'year': 2010
    })
    book_id = create_res.get_json()['id']

    del_res = client.delete(f'/books/{book_id}')
    assert del_res.status_code == 204

    get_res = client.get(f'/books/{book_id}')
    assert get_res.status_code == 404


def test_create_book_missing_fields(client):
    response = client.post('/books', json={'title': 'Без автора'})
    assert response.status_code == 400