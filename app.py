
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import Movie, Director, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app. config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)


api = Api(app)
movie_ns = api.namespace('/movies')
director_ns = api.namespace('/directors')
genre_ns = api.namespace('/genres')


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Nested(GenreSchema)
    director_id = fields.Int()
    director = fields.Nested(DirectorSchema)


movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        result = movies_schema.dump(all_movies)

        director_id = request.args.get('director_id')
        if director_id:
            movie = Movie.query.filter(Movie.director_id == director_id)
            result = movies_schema.dump(movie)

        genre_id = request.args.get('genre_id')
        if genre_id:
            movie = Movie.query.filter(Movie.genre_id == genre_id)
            result = movies_schema.dump(movie)

        if genre_id and director_id:
            movie = db.session.query(Movie).filter(Movie.genre_id == genre_id, Movie.director_id == director_id)
            result = movies_schema.dump(movie)

        return result, 200

    def post(self):
        data = request.json
        try:
            db.session.add(Movie(**data))
            db.session.commit()
            return "Всё норм прошло", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        result = movie_schema.dump(movie)

        return result, 200

    def put(self, mid):
        data = request.json
        try:
            db.session.query(Movie).filter(Movie.id == mid).update(data)
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, mid):
        try:
            db.session.query(Movie).filter(Movie.id == mid).delete()
            db.session.commit()
            return "Данные удалены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_dir = Director.query.all()
        result = directors_schema.dump(all_dir)
        return result

    def post(self):
        data = request.json
        try:
            db.session.add(Director(**data))
            db.session.commit()
            return "Всё норм прошло", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@director_ns.route('/<int:mid>')
class DirectorView(Resource):
    def put(self, mid):
        data = request.json
        try:
            db.session.query(Director).filter(Director.id == mid).update(data)
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, mid):
        try:
            db.session.query.filter(Director.id == mid).delete()
            db.session.commit()
            return "Данные удалены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_dir = Genre.query.all()
        result = genres_schema.dump(all_dir)
        return result

    def post(self):
        data = request.json
        try:
            db.session.add(Genre(**data))
            db.session.commit()
            return "Всё норм прошло", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@genre_ns.route('/<int:mid>')
class GenreView(Resource):
    def put(self, mid):
        data = request.json
        try:
            db.session.query(Genre).filter(Genre.id == mid).update(data)
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, mid):
        try:
            db.session.query.filter(Genre.id == mid).delete()
            db.session.commit()
            return "Данные удалены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


if __name__ == '__main__':
    app.run()
