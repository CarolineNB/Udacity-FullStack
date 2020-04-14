import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    
    try:
      if len(categories) == 0:
        abort(404)
      
      format_categories = [category.format() for category in categories]
      return jsonify({
        'success': True,
        'categories': format_categories,
        'total_categories': len(format_categories)
      })

    except:
      abort(422)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.all()

    if len(questions) == 0:
      abort(404)

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    formatted_questions = [question.format() for question in questions]

    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': len(formatted_questions)
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one()
    try:
      if question == None:
        abort(404)
      
      question.delete()

      return jsonify({
        'success': True, 
        'question': question, 
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/create_questions', methods=['POST'])
  def create_question():
    try:
      req = request.get_json()
      r_question = req.get('question', None)
      r_answer = req.get('answer', None)
      r_difficulty = req.get('difficulty', None)
      r_category = req.get('category', None)

      new_question = Question(question=r_question, answer=r_answer, difficulty=r_difficulty, category=r_category)
      new_question.insert()

      return jsonify({
        'success': True, 
        'created': new_question.id, 
        'total_questions': len(Question.query.all())   
      })
    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_question():
    try:
      search_term = request.get_json('searchTerm')
      results = Question.query.filter(Question.question.islike('%' + search_term + '%'))

      if len(results) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'results': [result.format() for result in results],
        'total_questions': len(results)
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def category_questions(category_id):
    try:
      cat_questions = Question.query.filter(Question.category == category_id)
      if len(cat_questions) == 0:
        abort(404)
      return jsonify({
        'success': True,
        'questions': [question.format() for question in cat_questions],
        'total_questions': len(cat_questions)
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def next_question():
    try:
      prev_questions = request.get_json('previousQuestions')
      category = request.get_json('quiz_category')

      category_questions = Question.query.filter(Question.category == category)

      if len(category_questions) == 0:
        abort(404)

      all_questions = [question.id for question in category_questions]
      unasked = [question.id for question in all_questions if question not in prev_questions]

      if len(unasked) == 0:
        abort(404)

      random_question = random.choice(unasked)
      to_question = Question.query.filter(Question.id == random_question)

      if to_question is None:
        abort(404)

      return jsonify({
        'success': True, 
        'question': to_question.format()
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'sucess': False,
      'error': 422,
      'message': unprocessable
    }), 422
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "resource not found"
    }), 404
  return app

    