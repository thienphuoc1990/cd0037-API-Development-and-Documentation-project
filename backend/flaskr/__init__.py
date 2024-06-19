import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import cast, Integer

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    

    """
    DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = db.session.query(Category).all()
        categories_dict = {category.id: category.type for category in categories}

        return jsonify({
            "success": True,
            "categories": categories_dict
        })


    """
    DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = db.session.query(Question).all()
        formatted_questions = [question.format() for question in questions]
        categories = db.session.query(Category).all()
        categories_dict = {category.id: category.type for category in categories}

        return jsonify({
            "success": True,
            "questions": formatted_questions[start:end],
            "total_questions": len(formatted_questions),
            "categories": categories_dict,
            "current_category": ''
        })

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = db.session.query(Question).get(question_id)

        if question is None:
            abort(422)

        question.delete()

        return jsonify({
            "success": True,
            "message": "Question successfully deleted"
        })

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        data = request.get_json()

        if (data["question"] is None or data["answer"] is None or
            data["difficulty"] is None or data["category"] is None):
            abort(422)

        Question(
            question=data["question"],
            answer=data["answer"],
            difficulty=data["difficulty"],
            category=data["category"]
        ).insert()

        return jsonify({
            "success": True,
            "message": "Question successfully created"
        })

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        data = request.get_json()
        search_term = data["searchTerm"]

        questions = db.session.query(Question).filter(Question.question.ilike(f"%{search_term}%")).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            'current_category': None
        })

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        questions = db.session.query(Question).filter(cast(Question.category, Integer) == category_id).all()
        current_category = db.session.query(Category).get(category_id)
        
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": current_category.type if current_category else 0
        })

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        data = request.get_json()
        previous_questions = data["previous_questions"]
        quiz_category = data["quiz_category"]

        if quiz_category["id"] == 0:
            questions = db.session.query(Question).filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = (db.session.query(Question).filter(cast(Question.category, Integer) == quiz_category["id"])
                            .filter(Question.id.notin_(previous_questions)).all())

        if len(questions) == 0:
            abort(404)

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "question": random.choice(formatted_questions)
        })

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """    
    @app.errorhandler(400)
    def bad_request(error):
        """
        Error handler for 400
        """
        return jsonify({
            "success": False,
            "message": "Bad Request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """
        Error handler for 404
        """
        return jsonify({
            "success": False,
            "message": "Not Found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """
        Error handler for 422
        """
        return jsonify({
            "success": False,
            "message": "Unprocessable Entity"
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Error handler for 500
        """
        return jsonify({
            "success": False,
            "message": "Internal Server Error"
        }), 500

    return app

