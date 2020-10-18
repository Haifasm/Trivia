# Full Stack Trivia 

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game to see who's the most knowledgeable of the bunch.

The application's frontend is implemented with React and the backend includes Flask and SQLAlchemy server.
The application is able to:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.
<img width="1435" alt="Screen Shot 2020-10-18 at 10 47 20 AM" src="https://user-images.githubusercontent.com/51233872/96361747-fd421180-1130-11eb-9f77-5b1f8dc2d489.png">

# Installation

Start by reading the READMEs in:
1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

It is recommended to follow the instructions in those files in order.

# API Reference

## Getting Started

This app can only be run locally, no authentication or API keys required.
1. The backend app is hosted at http://127.0.0.1:5000/.
2. Rhe frontend app is hosted at http://127.0.0.1:3000/. There is no requirement for authentication.

## Error Handling

Errors are returned in the following json format:
'''javascript
{
  'success': False,
  'error': 404,
  'message': 'Not Found'
}
'''

The errors handled by the API include:
- 400: Bad Request
- 404: Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error


