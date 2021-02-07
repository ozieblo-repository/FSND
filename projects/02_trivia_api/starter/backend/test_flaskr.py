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
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)
        setup_db(self.app,
                 self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # https://knowledge.udacity.com/questions/422782

    def test_get_categories(self):

        response = self.client().get('/categories')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    def test_404_sent_requesting_non_existing_category(self):

        response = self.client().get('/categories/7777')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions(self):

        response = self.client().get('/questions')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_request_beyond_valid_page(self):

        # invalid page data and then load response
        response = self.client().get('/questions?page=100')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_successful_delete_specific_question(self):

        question = Question(question='This is a mock test question.',
                            answer='This is a mock test answer.',
                            difficulty=1,
                            category='1')

        question.insert()

        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')

        data = json.loads(response.data)

        question = Question.query.filter(Question.id == question.id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(data['message'], "Question successfully deleted")
        self.assertEqual(question, None)

    def test_delete_question_with_invalid_id(self):

        # invalid id
        response = self.client().delete('/questions/asdfasdfasdf')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_question(self):

        response = self.client().post('/questions',
                                      json={'question': 'This is a question',
                                            'answer': 'This is a answer',
                                            'difficulty': 1,
                                            'category': 1})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')

    def test_422_if_question_creation_fails(self):

        # empty question data for failed delete request
        response = self.client().post('/questions',
                                      json={'question': '',
                                            'answer': '',
                                            'difficulty': 1,
                                            'category': 1})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_questions_multi_word(self):

        # valid multi word term
        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'Cassius Clay'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_search_questions_single_character(self):

        # valid single character input
        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'a'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_search_term_not_found(self):

        # a search request for the term that is not in the database and process response
        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'qwertyuiop'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_by_category(self):

        response = self.client().get('/categories/1/questions')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_if_questions_by_category_fails(self):

        # send an invalid category ID of 666, which does not exist
        response = self.client().get('/categories/666/questions')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_404_get_questions_per_category(self):

        response = self.client().get('/categories/a/questions')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_play_quiz_questions(self):

        response = self.client().post('/quizzes',
                                      json={'previous_questions': [5, 9],
                                            'quiz_category': {'type': 'Science',
                                                              'id': 1}})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)

        # check if questions from a previous quiz are not returned
        self.assertNotEqual(data['question']['id'], 5)
        self.assertNotEqual(data['question']['id'], 9)

    def test_no_data_to_play_quiz(self):

        # Process the response from the request without sending data
        response = self.client().post('/quizzes',
                                      json={})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()