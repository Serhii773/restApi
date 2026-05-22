from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from api.books import BookListResource, BookResource


def create_app():
    app = Flask(__name__)

    api = Api(app)

    Swagger(app, template={
        "info": {
            "title": "Library API",
            "description": "API для управління бібліотекою (Lab 5 - Flask + Swagger)",
            "version": "1.0.0"
        }
    })

    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<string:book_id>')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)