# Trivia App
This app is a game app that displays questions randomly from various categories, there is a input section for you to fill in the answer, if you get it right you will get a success message and if otherwise you will be notified.

I'm happy to have completed this trivia app. It gave me the ability to structure plan, implement, and test an API - skills essential for enabling your applications to communicate with others.


## Getting Started with the Project

This app is a fullstack app built with react and flask
[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine.

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip, node and npm installed on their local machines.


#### Backend

Navigate to backend directory and run `pip install -r requirements.txt` in the terminal. All required packages are included in the requirements file.

To start the server and run the application, run the following commands in the terminal: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

```

This starts the server, puts the app in development mode and directs the app to run the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default which is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands in the terminal: 
```
npm install // only once to install dependencies
npm start // to start the application in development mode

```
```npm starts``` start the client server in development mode

### Tests
In order to run tests traverse to the backend folder and run the following commands: 

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are written in ```test_flaskr.py``` file and should be maintained as updates are added to app. 

## API Referencing

### Getting Started
- Base URL: Presently, this app can only run locally and is not hosted as a base URL on a remote server. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

- Authentication: The present version of the app does not require authentication or API keys(until further updates).

### Error Handling
Errors are returned as JSON objects in the brlow format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not Alowed
- 422: Not Processable 

#### GET /categories
- General:
    - Returns a list containing a key/value pair of id as key and each category as value and a success value (True or False)

- Sample: `curl http://127.0.0.1:5000/categories`

```
{
    'categories': { 
     '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}

```

#### GET /questions?page=${integer}

Fetches a paginated set of questions, a total number of questions, all categories and current category string.

Request Arguments: page(integer)

Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

- Sample: `curl http://127.0.0.1:5000/questions?page=2`

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 50,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

#### GET /categories/${id}/questions

Fetches questions for a cateogry specified by id request argument

Request Arguments: id (integer)

Returns: An object with questions for the specified category, total questions, and current category string

- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 50,
    'currentCategory': 'History'
}
```

#### DELETE /questions/${id}

Deletes a specified question using the id of the question if exists

Request Arguments: id (integer)

Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

-Sample `curl -X DELETE http://127.0.0.1:5000/questions/11?page=2`

#### POST /quizzes

Sends a post request in order to get a random

Request Body:

```
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
 ```

Returns: a single new question object

-Sample `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d {"category":"2", "previous_question":"[2, 5, 7]", "rating":"5"}'`

```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```

#### POST /questions

Sends a post request in order to add a new question
Request Body:

Does not return a new data

-Sample `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`

```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```

#### POST /questions

Sends a post request in order to search for a specific question by search term recieved from the front end

Request Body:
```
{
    'searchTerm': 'your search term here'
}
```

Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```


## Deployment N/A
N/A

## Authors
Yours truly, Hassan Yahya 

## Acknowledgements 
Sunday Ajiroghene and all awesome students and tutuors at Udacity, soon to be full stack extraordinaires !
