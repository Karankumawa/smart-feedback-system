import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db, User, Feedback

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

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
