import os
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
  cors = CORS(app, resources={'/': {"origins": "*"}})


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    #used categories in response -> TypeError: Object of type Category is not JSON serializable so have to format categories!!
    #formatted_categories = [category.format() for category in categories] -> works in list but in 'add' got error
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type

    if len(formatted_categories) == 0:
          abort(404)
    
    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(Category.query.all())
    }), 201
  
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
  def paginate_questions(request, selection):
      #use request to be able to use its arguments to get the page number or 1 if no page number
      page = request.args.get('page', 1, type=int)
      #srart and end of the questions
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [question.format() for question in selection]
      current_questions = questions[start:end]

      return current_questions
  
  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    
    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.order_by(Category.id).all()
    #formatted_categories = [category.format() for category in catogeries] error
    formatted_categories = {category.id: category.type for category in categories}
    
    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': formatted_categories,
      'current_category': None
    }), 201
    
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      
      question.delete()

      #get questions after deleting and update pages
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      }), 201
    
    except:
      abort(400)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
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
  def create_question():

    body = request.get_json()
    
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    searchTerm = body.get('searchTerm', None)
    
    #search
    if searchTerm:
      #ILIKE allows you to perform case-insensitive pattern matching
      selection = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
      results = paginate_questions(request, selection)
      
      if len(results) == 0:
        abort(404)

      return jsonify({ #check paginattion
        'success': True,
        'questions': results,
        'total_questions': len(Question.query.all()),
        'number_of_results': len(results)
      }), 201
    
    #create
    else:
      try:
        question = Question(question = new_question, answer = new_answer, category = new_category, difficulty = new_difficulty)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        }), 201
      
      except:
        abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_in_category(id):
    #check if exist
    category = Category.query.filter_by(id = id).one_or_none()
    if category is None:
      abort(404)
    
    questions = Question.query.filter_by(category = str(id)).all()
    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
        abort(404)
    
    return jsonify({
        'success': True,
        'current_category': category.type,
        'questions': current_questions,
        'total_questions': len(current_questions)
      }), 201

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
  def play_quiz():

    data = request.get_json()
    quiz_category = data.get('quiz_category', None)
    previous_questions = data.get('previous_questions', [])

    if quiz_category is None:
      abort(404)

    # quiz_category -> ex. {'type': 'Science', 'id': '1'} get the id
    category_id = int(quiz_category['id'])

    try:
      # if id=0 all categories
      if category_id == 0:
        questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        questions = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previous_questions)).all()
      
      # get a random question from the available questions
      if questions:
        question = random.choice(questions)
        question_formatted = question.format()
      else:
        question_formatted = False
      
      return jsonify({
        'success': True,
        'previous_questions': previous_questions,
        'question': question_formatted
      }), 200
    except:
      abort(500)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 400 and 500.
  '''

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
      }), 404


  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
      }), 500
  
  return app

    