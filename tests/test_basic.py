import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db, User, Feedback
from flask_login import login_user

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['MONGODB_SETTINGS'] = {
            'db': 'test_db',
            'host': 'mongomock://localhost',
            'connect': False,
        }
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        User.drop_collection()
        Feedback.drop_collection()
        self.app_context.pop()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_sentiment_logic(self):
        from analysis import analyze_sentiment
        label, score = analyze_sentiment("I love this project!")
        self.assertEqual(label, "Positive")
        
        label, score = analyze_sentiment("This is terrible.")
        self.assertEqual(label, "Negative")

if __name__ == "__main__":
    unittest.main()
