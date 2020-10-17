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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the nearest planet to the sun?',
            'answer': 'Mercury',
            'difficulty': 2,
            'category': 1
        }
            
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
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
    Get Categories
    '''
    def test_get_categories(self):
        results = self.client().get('/categories')
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6) # total_categories = 6

    '''
    Get Questions
    '''
    #200
    def test_get_questions(self):
        results = self.client().get('/questions')
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions']) 
        self.assertEqual(len(data['questions']), 10) # 10 questions in the page
    
    #404 page doesn't exist
    def test_404_get_questions_beyond_pages(self):
        results = self.client().get('/questions?page=2000')
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not Found')
    
    '''
    Create Question
    '''
    def test_create_question(self):
        results = self.client().post('/questions', json=self.new_question)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 201) 
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    
    def test_405_create_question(self):
        results = self.client().post('/questions/1', json=self.new_question)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 405) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed') 
    
    '''
    Delete Question
    '''

    def test_delete_question(self):
        results = self.client().delete('/questions/2')
        data = json.loads(results.data)

        deleted_question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(results.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],2)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(deleted_question,None)

    def test_422_delete_question(self):
        results = self.client().delete('/questions/2000')
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    
    '''
    Get Question in Category
    '''
    def test_get_questions_in_category(self):
        results = self.client().get('/categories/1/questions')
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
    
    '''
    Play Quiz
    '''
    def test_play_quiz(self):
        results = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['previous_questions'], [])
        self.assertTrue('question')
    
    def test_404_play_quiz(self):
        results = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": None})
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
    
    '''
    Search
    '''
    def test_search(self):
        search = {
                'searchTerm': 'what',
        }
        results = self.client().post('/questions', json=search)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_404_search(self):
        search = {
                'searchTerm': 'zzzzzz',
        }
        results = self.client().post('/questions', json=search)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not Found')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

#python test_flaskr.py