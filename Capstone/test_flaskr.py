import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtnekozVTAyaGFvWkwwajJDMmdEVSJ9.eyJpc3MiOiJodHRwczovL2NiLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYmM3MTkyZGNlODBjNmYxODBmZDIiLCJhdWQiOiJDYXN0cyIsImlhdCI6MTU5MDM0NTA5MywiZXhwIjoxNTkwNDMxNDkzLCJhenAiOiJ6SnV0WDJNbEVyalRUTEpPT0FCT0dnekdyWTFiTkVnTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.JxCPSfykwtuU6vm4vK2ALfu-VH2hZVZilzDBNF940qw8ZUy_9pPOXOu55dttHTtxe4YMjROidlT4tIWTTkynYqvUmUCGpn_2xa-r1vC5Uv1__CP_GE2oqEZZYp2ZccClPABxl-XLOK1MVPFIJpo368cnA-YqlkJOKipckSVahpCh11MCnaLe8pZcZXPrezDGJm-iSFhSRx_IBe2RDFt8m07ChvUOPgm44aZSp-K74ynRpIpyO3UbPK8It2tRLU061H-IxHsnVI_Os4VcwOnxMyPo4I8oe5RrfH9DiZU1XJkbmYw5miLuGOYm3XtUzyV2mRNtlO3Vi4Wqtl3FD34z_g"
        self.director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtnekozVTAyaGFvWkwwajJDMmdEVSJ9.eyJpc3MiOiJodHRwczovL2NiLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYmQwMWVlNTZjNDBjNmQ4NTRmZDYiLCJhdWQiOiJDYXN0cyIsImlhdCI6MTU5MDM0NTEzOCwiZXhwIjoxNTkwNDMxNTM4LCJhenAiOiJ6SnV0WDJNbEVyalRUTEpPT0FCT0dnekdyWTFiTkVnTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicG9zdDphY3RvcnMiXX0.CwZtkWTEhdIR-I2f0cHrwomKZjHZ9s21Un13JqvPRArXETG38MldfORnkdwMLlQUH2TOsoyug4NvaeHTVSc5MTiYU6W_OJgovaZcBZQlUqNMyeyJ9wRN0qO4im-NOgYPMU3_02VTBZNLOMCtICoQSj96LB6f8jYzwIJAV5FYLMdFpM9mYtx9-_fvIk6xhwMPJ9RLvdmPNlPoiZtiaDJrXHYtKkvwmzniUGGdqIDD1yWf5uwnT0QU_7H-rrkE81HDXI_D67D305qruvvZbQvdbjvwJkVNtA4OTFse0-mqigz8TG7Rw6Fd8TdtE-c9HjMPgHwYc9dhVsxTV8V_MXmR2A"
        self.producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtnekozVTAyaGFvWkwwajJDMmdEVSJ9.eyJpc3MiOiJodHRwczovL2NiLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYmQyMTkyZGNlODBjNmYxODE0M2UiLCJhdWQiOiJDYXN0cyIsImlhdCI6MTU5MDM0NTE3OSwiZXhwIjoxNTkwNDMxNTc5LCJhenAiOiJ6SnV0WDJNbEVyalRUTEpPT0FCT0dnekdyWTFiTkVnTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.gwf1KR3__LT4qq1f_ZEgn1i714j3Dc56BUjnXHPj9frU-PPiGBQwahOirDlVO7Nl8lP-XhLGwTGvTixxz5p-Zzs7tUTngUNxpjxIqjv5dG63iYYslXJm9mh3hx_CFC4AFdi8MMKWrI3iU0zKLXmPbnHGZiW8EBqAapuzWBdNi08wTRRGGPMxE_NGwVcy7jFOva7QAqo3fO0W804Ejx8o4eG9itSPHTnKAbg5RUwT5KHyL8BzhnTHlzAj2kmtWLBr8yvGxOt3wqkGxAfyBWzdYnSzes7vRvAR71BzPfEOAf8ipLJCusycf0s4-WJ3LT6m2hVF_NFSGMEPRgVaq9ORiA"
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
                                headers={'Authorization': 'Bearer '+self.assistant})
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
                                headers={'Authorization': 'Bearer '+self.assistant})
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
                                   headers={'Authorization': 'Bearer '+self.director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_producer(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization': 'Bearer '+self.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_error_assistant(self):
        res = self.client().delete('/actors/4',
                                   headers={'Authorization': 'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_invalid(self):
        res = self.client().delete('/actors/999',
                                   headers={'Authorization': 'Bearer '+self.director})
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
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
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
        res = self.client().patch('/actors/5',
                                 headers={
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
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
                                     "Authorization": "Bearer {}".format(
                                         self.producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()