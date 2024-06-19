import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('postgres', 'localhost:15432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

        self.seedData(self)

    
    @classmethod
    def tearDownClass(self):
        """Executed after reach test"""
        db.drop_all()
        pass

    def seedData(self):
        Category(
            type="Science"
        ).insert()
        Category(
            type="Art"
        ).insert()

        Question(
            question="What boxer's original name is Cassius Clay?",
            answer="Muhammad Ali",
            difficulty=1,
            category=1
        ).insert()
        Question(
            question="What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
            answer="Tom Cruise",
            difficulty=4,
            category=2
        ).insert()


    """
    DOING
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET /notfoundurl
    def test_get_notfound_url(self):
        res = self.client().get("/notfoundurl")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not Found")

    # GET /categories
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["categories"], {
            "1": "Science",
            "2": "Art"
        })

    # GET /questions
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"],
            [
                {'answer': 'Muhammad Ali', 'category': '1', 'difficulty': 1, 'id': 1, 'question': "What boxer's original name is Cassius Clay?"}, 
                {'answer': 'Tom Cruise', 'category': '2', 'difficulty': 4, 'id': 2, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'}
            ]
        )
        self.assertEqual(len(data["questions"]), 2)
        self.assertEqual(data["categories"], {
            '1': 'Science', '2': 'Art'
        })


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()