import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
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

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    def test_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        self.assertEqual(res.status_code, 200)

    def test_404_delete_invalid_question(self):
        res = self.client().delete('/questions/1000')
        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        question = {
            'question': 'this is a question',
            'answer': 'this is an answer',
            'category': 1,
            'difficulty': 1
        }
        res = self.client().post('/create_questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    def test_404_create_invalid_question(self):
        question = {
            'question': 3,
            'answer': 'this is an answer',
            'category': 'not a category',
            'difficulty': 'not a difficulty'
        }

        res = self.client().post('/create_questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_search_term(self):
        res = self.client().post('/questions', json={'searchTerm': 'who'})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_invalid_search(self):
        res = self.client().post('/questions', json={'searchTerm': '--0--'})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['category']['id'], 1)

    def test_404_get_question_by_invalid_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quizzes(self):
        body = {
            'previous_questions': [2, 4],
            'category_id': 5,
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
