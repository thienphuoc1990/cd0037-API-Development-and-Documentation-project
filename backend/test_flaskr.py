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
        self.app = create_app()

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
            category=2).insert()

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
                         [{'answer': 'Muhammad Ali',
                           'category': '1',
                           'difficulty': 1,
                           'id': 1,
                           'question': "What boxer's original name is Cassius Clay?"},
                          {'answer': 'Tom Cruise',
                           'category': '2',
                           'difficulty': 4,
                           'id': 2,
                           'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'}])
        self.assertEqual(len(data["questions"]), 2)
        self.assertEqual(data["categories"], {
            '1': 'Science', '2': 'Art'
        })

    def test_get_questions_by_page(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["categories"], {
            '1': 'Science', '2': 'Art'
        })

    def test_delete_question_fail(self):
        res = self.client().delete("/questions/999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_post_question_fail(self):
        res = self.client().post("/questions", json={
            "question": "Test question",
            "answer": None,
            "difficulty": 1,
            "category": 1
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable Entity")

    # POST /questions
    def test_post_and_delete_question(self):
        res = self.client().post("/questions", json={
            "question": "Test question",
            "answer": "Test answer",
            "difficulty": 1,
            "category": 1
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question successfully created")
        self.assertTrue(data["success"])

        # DELETE /questions/<int:question_id>
        res = self.client().delete("/questions/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    # POST /questions/search
    def test_search_questions(self):
        res = self.client().post("/questions/search", json={
            "searchTerm": "Cassius"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"],
                         [{'answer': 'Muhammad Ali',
                           'category': '1',
                           'difficulty': 1,
                           'id': 1,
                           'question': "What boxer's original name is Cassius Clay?"},
                          ])
        self.assertEqual(data["total_questions"], 1)

    def test_search_questions_not_found(self):
        res = self.client().post("/questions/search", json={
            "searchTerm": "not found text"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["total_questions"], 0)

    # GET /categories/<int:category_id>/questions
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"],
                         [{'answer': 'Muhammad Ali',
                           'category': '1',
                           'difficulty': 1,
                           'id': 1,
                           'question': "What boxer's original name is Cassius Clay?"},
                          ])
        self.assertEqual(data["total_questions"], 1)

    def test_get_questions_by_category_not_found(self):
        res = self.client().get("/categories/999/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(data["current_category"], 0)

    # POST /quizzes
    def test_get_quiz_question(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {
                "id": 0,
                "type": "All"
            }
        })

        data = json.loads(res.data)

        print(data["question"])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_get_quiz_question_fail(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {
                "id": 999,
                "type": "All"
            }
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not Found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
