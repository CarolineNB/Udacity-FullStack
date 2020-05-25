# Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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

## Running the server

Within this directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Getting Started
This app handles users with multiple roles:
 - _Casting Assistant_
    - Can view actors and movies 
 - _Casting Director_
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
 - _Executive Producer_
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## Error Handling

Errors are returned in JSON objects in the following format:
```
{
  'success': False,
  'error': 404,
  'message': "resource not found"
}
```
This API will return the following error types when requests fail:
  - 400
  - 401
  - 404
  - 422
  - 500


## Testing
To run the tests, run

```
dropdb capstone_test
createdb capstone_test
psql capstone_test < db.psql
python test_flaskr.py
```

## Endpoints

### GET `/movies`

- General:
  - Fetches a list of all movies.
  - Request Arguments: None
  - Access Requirements: Assistant, Director, or Producer
  - Returns: JSON objects containing movies including their name and date produced. 
- Sample: `http://127.0.0.1:5000/movies`
```
"movies": [
        {
            "date": 2019,
            "id": 1,
            "name": "22"
        },
        {
            "date": 1998,
            "id": 2,
            "name": "Horizon"
        },
       ...
        {
            "date": 2000,
            "id": 6,
            "name": "Forever 15"
        }
    ],
    "success": true,
    "total movies": 6
```

### GET `/actors`

- General:
  - Fetches a list of all actors
  - Request Arguments: None
  - Access Requirements: Assistant, Director, or Producer
  - Returns: JSON objects containing movies including their name, age, and gender. 
- Sample: `http://127.0.0.1:5000/actors` 
```
"actors": [
        {
            "age": 24,
            "gender": "female",
            "id": 1,
            "name": "Ellie"
        },
        {
            "age": 29,
            "gender": "female",
            "id": 3,
            "name": "Jess"
        },
        ...
        {
            "age": 18,
            "gender": "male",
            "id": 2,
            "name": "Andrew"
        }
    ],
    "success": true,
    "total actors": 5
```

### DELETE `/actors/<int:actor_id>`
- General:
  - Deletes an actor using their ID 
  - Request Arguments: None
  - Access Requirements: Director or Producer
  - Returns: Deletes a question using its corresponding id.
  - Sample: `http://127.0.0.1:5000/actors/1` 
```
{
    "actor": 1,
    "success": true
}
```

### POST `/movies`

- General:
  - Creates an movie entry given a JSON object with the correct arguments
  - Request Arguments: JSON object with name and year produced
  - Access Requirements: Producer
```
{
    "name": "IT", 
    "year": 2017
}
```

### POST `/actors`

- General:
  - Creates an actor entry given a JSON object with the correct arguments
  - Request Arguments: JSON object with age, gender, and name.
  - Access Requirements: Director or Producer
```
{
    "age": 45,
    "gender": "Female",
    "name": "Mary"
}
```

 
 ### PATCH `/actors`
 
 -General:
  -Edits an actor's entry given a JSON object with the correct arguments
  -Request Arguments: JSON object with id, gender, age, and name
```
{
    "age": 29,
    "gender": "female",
    "id": 3,
    "name": "Jessie" #from Jess to Jessie
}
```
  -Returns: Updated values
```
{
    "actor": "Jessie",
    "success": true
}
```
