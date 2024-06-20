# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

Copy the file .env.example to .env and update the variable.
Run docker-compose from root project with command
```bash
docker-compose up -d
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql -hlocalhost -Upostgres trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

### `GET '/categories'`
  
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
  }
}
```

### `GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category.
- Request Arguments: `page` - integer
- Returns: An object with list of paginated question items, total questions, all categories, and current category

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What boxer's original name is Cassius Clay?",
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 2,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "category": 2,
      "difficulty": 4
    }
  ],
  "total_questions": 2,
  "categories": {
    "1": "Science",
    "2": "Art",
  },
  "current_category": "Science"
}
```

### `DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: A message

```json
{
  "success": true,
  "message": "Question successfully deleted"
}
```

### `POST '/questions'`

- Sends a post request to add a new question
- Request Body: 

```json
{
  "question": "question string",
  "answer": "answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: A message

  ```json
  {
    "success": true,
    "message": "Question successfully created"
  }
  ```

### `POST '/questions/search'`
  
- Sends a post request to search questions by search term
- Request Body:

```json
{
  "searchTerm": "search term string"
}
```

- Returns: An object with list of questions, total questions and current category.

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What boxer's original name is Cassius Clay?",
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 2,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "category": 2,
      "difficulty": 4
    }
  ],
  "total_questions": 2,
  "current_category": "Science"
}
```

### `GET '/categories/${id}/questions'`
  
- Fetches questions of category by category id
- Request Arguments: `id` - integer
- Returns: An object with questions for the requested category, total questions, and current category

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What boxer's original name is Cassius Clay?",
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 2,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "category": 2,
      "difficulty": 4
    }
  ],
  "total_questions": 2,
  "current_category": "Science"
}
```

### `POST '/quizzes'`

- Sends a post request to get the next random question
- Request Body:

```json
{
  "previous_questions": [1],
  "quiz_category": "Science"
}
```

- Returns: a single new question object

```json
{
  "success": true,
  "question": {
    "id": 2,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
    "answer": "Tom Cruise",
    "category": 2,
    "difficulty": 4
  }
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run
```bash
docker-compose up -d
```

```bash
DB_NAME='trivia_test' DB_USER='postgres' DB_PASSWORD='postgres' DB_HOST='localhost' DB_PORT='15432' python test_flaskr.py
```
![Test result](./docs/assets/test_result.png)