import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from flask_cors import CORS
import random
import sys

from .databases.models import setup_db, Movie, Actor
from .auth.auth import AuthError, requires_auth



def create_app(test_config=None):
    #create and configure app
    app = Flask(__name__)
    CORS(app)

    setup_db(app)
    #set access control allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, \
          PATCH, DELETE, OPTIONS')
        return response

    
    @app.route('/')
    def get_greeting():
        greeting = "Hello" 
        return greeting


    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)
            
        return jsonify({
            'success': True, 
            'movies': movies, 
            'total movies': len(movies)
        }), 200

    
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)
        
        return jsonify({
            'success': True, 
            'actors': actors, 
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
            'created': "name: " + new_actor.name + " id: " + new_actor.id,
            'total actors': len(Actors.query.all())
        }), 200
    return app


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        body = request.get_json()
        a_name = body.get('name', None)
        a_date= body.get('date', None)

        new_movie = Movie(
            name=a_name,
            date=a_date
        )

        new_movie.insert()

        return jsonify({
            'success': True,
            'created': "name: " + new_movie.name + " id: " + new_movie.id,
            'total movies': len(Movies.query.all())
        }), 200
    return app

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, actor_id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)
        
        try:
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
        except Exception:
            abort(400)
        
        return jsonify({'sucess':True, 'actor':a_name}), 200


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_more()
            if not movie:
                abort(404)
            
            movie.delete()

            return jsonify({
                'sucess': True,
                'movie': movie_id
            }), 200
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_more()
            if not actor:
                abort(404)
            
            actor.delete()

            return jsonify({
                'sucess': True,
                'movie': actor_id
            }), 200
        except Exception:
            abort(422)


app = create_app()

if __name__ == '__main__':
    app.run()


# Error Handling
'''
Example error handling for unprocessable entity
'''
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
        "messange": "unauthorized"
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