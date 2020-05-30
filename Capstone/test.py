import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant = os.environ.get('assistant_token')
        self.director = os.environ.get('director_token')
        self.producer = os.environ.get('producer_token')
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres: @localhost:5432/{}"\
            .format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total actors'], len(Actor.query.all()))

    def test_get_actors_invalid_permission(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total movies'], len(Movie.query.all()))

    def test_get_movies_invalid_permission(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_director(self):
        res = self.client().delete('/actors/2',
                                   headers={'Authorization':
                                            'Bearer '+self.director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_producer(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization':
                                            'Bearer '+self.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_error_assistant(self):
        res = self.client().delete('/actors/4',
                                   headers={'Authorization':
                                            'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_invalid(self):
        res = self.client().delete('/actors/999',
                                   headers={'Authorization':
                                            'Bearer '+self.director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_actor_producers(self):
        actor = {
            'name': 'name2',
            'gender': 'gender2',
            'age': 22
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_director(self):
        actor = {
            'name': 'name',
            'gender': 'gender',
            'age': 20
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.director)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_producer(self):
        actor = {
            'name': 'name2',
            'gender': 'gender2',
            'age': 22
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_producers(self):
        actor = {
            'name': 'changename',
            'gender': 'gender2',
            'age': 223
        }
        res = self.client().patch('/actors/7',
                                  headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                  }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_director(self):
        actor = {
            'name': 'changeNameAgain',
            'gender': 'gender2',
            'age': 223
        }
        res = self.client().patch('/actors/6',
                                  headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.director)
                                  }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_assistant_error(self):
        actor = {
            'name': 'changeNameAgain',
            'gender': 'gender2',
            'age': 223
        }
        res = self.client().patch('/actors/3',
                                  headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.assistant)
                                  }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        movie = {
            'name': 'this is a name',
            'date': 100799
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_director_error(self):
        movie = {
            'name': 'this is a name',
            'date': 100799
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.director)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie_invalid(self):
        movie = {
            'name': 333,
            'date': 100799
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
