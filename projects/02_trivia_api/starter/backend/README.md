# Full Stack Trivia API Backend

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Style guideline
backend code follows PEP8

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## How to run the app using the frontend

The `./frontend` directory contain a complete React frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)


## Tasks

Define the endpoint and response data. 
The frontend is set up to expect certain endpoints and response data formats already.

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a GET endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

### `GET '/categories'` :
- handle requests for all available categories
- fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- request arguments: None
- category key:value is 1 = Science, 2 = Art, 3 = Geography, 4 = History, 5 = Entertainment, 6 = Sports

```
(FSND) Michas-MBP:backend michalozieblo$ curl http://localhost:3000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}

```

### `GET '/questions'` : 
- handle requests for questions, including pagination (every 10 questions). 
- return a list of questions, number of total questions, current category, categories. 
- request arguments: None

```
(FSND) Michas-MBP:backend michalozieblo$ curl http://localhost:3000/questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 25
}
```

### `DELETE '/questions/<int:question_id>'` : 
- an endpoint to remove question using a question ID.
- request argument: question ID

```
(FSND) Michas-MBP:backend michalozieblo$ curl http://localhost:3000/questions/16 -X DELETE
{
  "deleted": 16, 
  "message": "Question successfully deleted", 
  "success": true
}
```

### `POST '/questions'` : 
- insert a new question, which will require the question and answer text, category, and difficulty score.
- request arguments: None

```
(FSND) Michas-MBP:backend michalozieblo$ curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d "{\"question\": \"test\", \"answer\":\"test\", \"category\":\"4\", \"difficulty\":\"3\"}"
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "message": "Question successfully created!", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 25
}
```


### `POST '/questions/search'` : 
- get questions based on a search term. 
- return any questions for whom the search term is a substring of the question. 
- request arguments: None

```
(FSND) Michas-MBP:backend michalozieblo$ curl http://localhost:3000/questions/search -X POST -d '{"searchTerm":"Tom"}' -H "Content-Type: application/json"
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### `GET '/categories/<int:id>/questions'` : 
- get questions based on category. 
- request argument: category ID

```
(FSND) Michas-MBP:backend michalozieblo$ curl http://localhost:3000/categories/2/questions
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 24
}
```

### `POST '/quizzes'` : 
- get questions to play the quiz. 
- take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
- request arguments: None

```
(FSND) Michas-MBP:backend michalozieblo$ curl -X POST "http://localhost:3000/quizzes" -d "{\"quiz_category\":{\"type\": \"History\", \"id\": \"4\"},\"previous_questions\":[2]}" -H "Content-Type: application/json"
{
  "question": {
    "answer": "Maya Angelou", 
    "category": 4, 
    "difficulty": 2, 
    "id": 5, 
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }, 
  "success": true
}

```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Udacity Knowledge
- https://knowledge.udacity.com/questions/413252 | Delete the sample route after completing the TODOs?
- https://knowledge.udacity.com/questions/378076 | Flask-CORS @app.after_request
- https://knowledge.udacity.com/questions/119096 | @app.route('/categories')
- https://knowledge.udacity.com/questions/233578 | @app.route('/categories')
- https://knowledge.udacity.com/questions/103865 | @app.route('/questions')
- https://knowledge.udacity.com/questions/125664 | @app.route('/questions')
- https://knowledge.udacity.com/questions/309862 | @app.route('/questions')
- https://knowledge.udacity.com/questions/439603 | @app.route('/questions/<int:question_id>', methods=['DELETE'])
- https://knowledge.udacity.com/questions/336412 | @app.route('/questions/search', methods=['POST'])
- https://knowledge.udacity.com/questions/421873 | @app.route('/categories/<int:id>/questions')
- https://knowledge.udacity.com/questions/58505 | @app.route('/quizzes', methods=['POST'])

