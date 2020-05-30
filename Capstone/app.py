import os
from flask import Flask, render_template, jsonify, request, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
import os
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__)
    CORS(app)

    setup_db(app)
    # set access control allow

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, \
          PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        greeting = "Hello! Welcome to Casting Agency!"
        return greeting

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            if len(movies) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': [movie.long() for movie in movies],
                'total movies': len(movies)
            }), 200

        except Exception as error:
            raise error

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.long() for actor in actors],
            'total actors': len(actors)
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(payload):
        body = request.get_json()
        a_name = body.get('name', None)
        a_age = body.get('age', None)
        a_gender = body.get('gender', None)

        new_actor = Actor(
            name=a_name,
            age=a_age,
            gender=a_gender
        )

        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.long(),
            'total actors': len(Actor.query.all())
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        body = request.get_json()
        a_name = body.get('name', None)
        a_date = body.get('date', None)

        new_movie = Movie(
            name=a_name,
            date=a_date
        )

        new_movie.insert()

        return jsonify({
            'success': True,
            'created': new_movie.long(),
            'total movies': len(Movie.query.all())
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'actor': actor_id
        }), 200

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, id):
        try:
            body = request.get_json()
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if not actor:
                abort(404)

            a_name = body.get('name')
            a_age = body.get('age')
            a_gender = body.get('gender', None)

            if a_name:
                actor.name = a_name

            if a_age:
                actor.age = a_age

            if a_gender:
                actor.gender = a_gender

            actor.update()

            return jsonify({'success': True, 'actor': a_name}), 200

        except Exception:
            abort(400)
    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "messange": "resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal service error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": "authorization error"
        }), error.status_code

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
