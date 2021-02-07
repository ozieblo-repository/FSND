# Full Stack API Final Project - Trivia

### PROJECT DESCRIPTION BELOW:

Udacity invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience was limited and needed to be built out. 

The task was to finish the Trivia app to allow start holding trivia and seeing who's the most knowledgeable of the bunch. 

The requirements were to provide options:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

The aim of the project was to give the student the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## About the Stack

The full stack application has been already started by Udacity. It was desiged with some key functional areas:

### Backend

The `./backend` directory contained a partially completed Flask and SQLAlchemy server. I have worked primarily in app.py to define endpoints and reference models.py for DB and SQLAlchemy setup. 

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contained a complete React frontend to consume the data from the Flask server. I needed to update the endpoints after I had defined them in the backend.

[View the README.md within ./frontend for more details.](./frontend/README.md)
