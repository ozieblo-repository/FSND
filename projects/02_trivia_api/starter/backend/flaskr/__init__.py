import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):

  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  # https://knowledge.udacity.com/questions/413252

  cors = CORS(app, resources={r"*": {"origins": "*"}})

  '''
  after_request decorator to set Access-Control-Allow
  '''

  # https://knowledge.udacity.com/questions/378076

  @app.after_request
  def after_request(response):

    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type, Authorization")

    response.headers.add("Access-Control-Allow-Methods",
                         "GET, POST, PATCH, DELETE, OPTIONS")

    return response

  '''
  an endpoint to handle GET requests for all available categories.
  '''

  # https://knowledge.udacity.com/questions/119096
  # https://knowledge.udacity.com/questions/233578

  @app.route('/categories')
  def get_categories():

      page = request.args.get('page', 1, type=int)

      start = (page - 1) * 10
      end = start + 10

      categories = Category.query.all()

      if len(categories) == 0:
          abort(404)

      formatted_categories = {category.id: category.type for category in categories}

      return jsonify({'success': True,
                      'categories': formatted_categories,
                      'total_categories': len(categories)})

  '''
  an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint return a list of questions, 
  number of total questions, current category, categories. 
  '''

  # https://knowledge.udacity.com/questions/103865
  # https://knowledge.udacity.com/questions/125664
  # https://knowledge.udacity.com/questions/309862

  def paginate_questions(request, questions_list):

      page = request.args.get('page', 1, type=int)

      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [question.format() for question in questions_list]

      paginated_questions = questions[start:end]

      return paginated_questions

  def get_category_list():

      categories = {}

      for category in Category.query.all():
          categories[category.id] = category.type

      return categories

  @app.route('/questions')
  def get_questions():

      questions_list = Question.query.all()
      paginated_questions = paginate_questions(request,
                                               questions_list)

      if len(paginated_questions) == 0:
          abort(404)

      return jsonify({'success': True,
                      'questions': paginated_questions,
                      'total_questions': len(questions_list),
                      'categories': get_category_list(),
                      'current_category': None})

  '''
  an endpoint to DELETE question using a question ID.
  '''

  # https://knowledge.udacity.com/questions/439603

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_specific_question(question_id):
      try:

          selected_question = Question.query.filter(Question.id == question_id).one_or_none()

          if selected_question is None:
              abort(404)

          selected_question.delete()

          return jsonify({'success': True,
                          'deleted': question_id,
                          'message': "Question successfully deleted"})
      except:
          abort(422)

  '''
  an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():

      data = request.get_json()

      question = data.get('question', '')
      answer = data.get('answer', '')
      difficulty = data.get('difficulty', '')
      category = data.get('category', '')

      selection = Question.query.all()
      total_questions = len(selection)
      current_questions = paginate_questions(request, selection)

      categories = Category.query.all()
      categories_dict = {}

      for cat in categories:
          categories_dict[cat.id] = cat.type

      if ((question == '') or (answer == '') or (difficulty == '') or (category == '')):
          abort(422)

      try:
          question = Question(question=question,
                              answer=answer,
                              difficulty=difficulty,
                              category=category)

          question.insert()  # save the question

          return jsonify({'success': True,
                          'message': 'Question successfully created!',
                          'questions': current_questions,
                          'total_questions': total_questions,
                          'categories': categories_dict}), 201

      except Exception:
          abort(422)

  '''
  POST endpoint to get questions based on a search term. 
  It return any questions for whom the search term 
  is a substring of the question. 
  '''

  # https://knowledge.udacity.com/questions/336412

  @app.route('/questions/search', methods=['POST'])
  def search_questions():

      try:
          search_term = request.json.get('searchTerm', None)
          questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
          formatted_questions = [question.format() for question in questions]

          if len(questions) == 0:
              abort(404)  # resource not found
          return jsonify({"success": True,
                          "questions": formatted_questions,
                          "total_questions": len(questions),
                          "current_category": None})
      except Exception as e:
          print("Exception is: ", e)
          abort(404)

  '''
  GET endpoint to get questions based on category. 
  '''

  # https://knowledge.udacity.com/questions/421873

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):

      category = Category.query.filter_by(id=id).one_or_none()

      if (category is None):
          abort(400)

      selection = Question.query.filter_by(category=category.id).all()

      paginated = paginate_questions(request, selection)

      return jsonify({'success': True,
                      'questions': paginated,
                      'total_questions': len(Question.query.all()),
                      'current_category': category.type})

  '''
  POST endpoint to get questions to play the quiz. 
  This endpoint take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''

  # https://knowledge.udacity.com/questions/58505

  @app.route('/quizzes', methods=['POST'])
  def play_quiz_question():

      body = request.get_json()
      previous = body.get('previous_questions')
      category = body.get('quiz_category')

      if ((category is None) or (previous is None)):
          abort(400)

      if (category['id'] == 0):
          questions = Question.query.all() # load all questions if "ALL" option is selected
      else:
          questions = Question.query.filter_by(category=category['id']).all()

      total = len(questions)

      def get_random_question():
          return questions[random.randrange(0, len(questions), 1)]

      def check_if_used(question):
          used = False
          for q in previous:
              if (q == question.id):
                  used = True
          return used

      question = get_random_question()

      while (check_if_used(question)):
          question = get_random_question()

          # when all questions have been asked, return without question (for <5 questions)
          if (len(previous) == total):
              return jsonify({'success': True})

      return jsonify({'success': True,
                      'question': question.format()})

  '''
  error handlers for all expected errors
  '''

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({"success": False,
                      "error": 400,
                      "message": "Bad request"}), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({"success": False,
                      "error": 404,
                      "message": "Resource not found"}), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({"success": False,
                      "error": 422,
                      "message": "Unprocessable"}), 422

  @app.errorhandler(500)
  def unprocessable(error):
      return jsonify({"success": False,
                      "error": 500,
                      "message": "Internal server error"}), 500

  return app