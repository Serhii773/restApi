from flask import request
from flask_restful import Resource
from repository.book_repository import BookRepository

repo = BookRepository()


class BookListResource(Resource):
    def get(self):
        """
        Отримати всі книги з пагінацією
        ---
        parameters:
          - name: skip
            in: query
            type: integer
            default: 0
          - name: limit
            in: query
            type: integer
            default: 10
        responses:
          200:
            description: Список книг
        """
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 10, type=int)
        books = repo.get_all(skip=skip, limit=limit)
        count = len(books)
        next_offset = skip + limit if count == limit else None

        return {
            'books': books,
            'pagination': {
                'limit': limit,
                'offset': skip,
                'next_offset': next_offset,
                'count': count,
                'message': f"Книги з {skip} по {skip + count}"
            }
        }, 200

    def post(self):
        """
        Створити нову книгу
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              $ref: '#/definitions/BookCreate'
        responses:
          201:
            description: Книгу створено
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Невалідні дані
        definitions:
          BookCreate:
            type: object
            required:
              - title
              - author
              - year
            properties:
              title:
                type: string
                example: "Кобзар"
              author:
                type: string
                example: "Тарас Шевченко"
              description:
                type: string
              status:
                type: string
                enum: ["наявні в бібліотеці", "видані комусь"]
                default: "наявні в бібліотеці"
              year:
                type: integer
                example: 1840
          Book:
            type: object
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              description:
                type: string
              status:
                type: string
              year:
                type: integer
        """
        data = request.get_json()
        if not data or not data.get('title') or not data.get('author') or not data.get('year'):
            return {'message': 'title, author та year є обовʼязковими'}, 400

        allowed = {'title', 'author', 'description', 'status', 'year'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        filtered.setdefault('status', 'наявні в бібліотеці')

        book = repo.add(filtered)
        return book, 201


class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Книгу знайдено
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Книгу не знайдено
        """
        book = repo.get_by_id(book_id)
        if not book:
            return {'message': 'Книгу не знайдено'}, 404
        return book, 200

    def delete(self, book_id):
        """
        Видалити книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Книгу видалено
          404:
            description: Книгу не знайдено
        """
        success = repo.delete(book_id)
        if not success:
            return {'message': 'Книгу не знайдено'}, 404
        return '', 204