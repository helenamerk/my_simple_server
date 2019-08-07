# Making A Server

## What is this?

This is a very basic REST API.

Postman is a _very_ helpful tool for testing requests: https://www.getpostman.com/downloads/

## What is REST?

Representational State Transfer (REST). It is a software architectural style for creating web services. It uses a uniform and predefined set of stateless operations.

## What rules define a REST system?

Great question! There's 6:

1. Client-Server: Seperation of power. Server (backend) that offers a service should be seperate from the the client (frontend) that consumes it.
2. Stateless: Isolated functionality. A client's request must contain all information for that request. ie the server should store information provided by the client in one request in order to use it in another request. _Note: this is different from storing something in a database._
3. Cacheable: Caching significantly improves performance. (I bet github does it with what you are reading rn!) The server must indicate if it caches to the client.
4. Layered System: Client can not tell if it is connected to an intermediary or not. ie. Communication between a client and a server allows intermediaries to respond to requests instead of the end server, without the client having to do anything different.
5. Uniform Interface: The method of communication between a client and a server must be uniform.
6. Code on demand (Optional): Servers can provide executable code or scripts for clients to execute in their context.

## What is a RESTful Web Service?

A standardized way of interacting with resources. Helpful tip -- include versioning to help with updates, and to prevent breaking older integrations,

| HTTP Method | What it do                      | Example                                                                  |
| ----------- | ------------------------------- | ------------------------------------------------------------------------ |
| GET         | Get me all users                | https://my-simple-server/api/1.0/users                                   |
| GET         | Get me information about user 2 | https://my-simple-server/api/1.0/users/2                                 |
| POST        | Add user                        | https://my-simple-server/api/1.0/users (with data provided in request)   |
| PUT         | Update user 3                   | https://my-simple-server/api/1.0/users/3 (with data provided in request) |
| DELETE      | Delete user 4                   | https://my-simple-server/api/1.0/users/4                                 |

Each _user_ will have the following attributes:

- username: (unique) String type.
- password_hash: String type.
- email: String type
- points: Integer type.

Implementing the first GET route, can be done almost imediately. The slightly more complex part comes when we connect it to a database.

```Python
from flask import Flask, jsonify

app = Flask(__name__)

user = [
    {
        'id': 1,
        'username': 'helenamerk',
        'password_hash': 'xyxyxyx',
        'email': 'helena.lmtm@gmail.com',
        'points': 1738
    },
    {
        'id': 2,
        'username': 'player2',
        'password_hash': 'xyxyxyx',
        'email': 'hello@customdomain.com',
        'points': 1506
    },
]

@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
```

Adding the path to get details of a single user/resource, is as easy as adding another endpoint:

```python
from flask import abort

@app.route('/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})
```

And adding a new user:

```python
from flask import request

@app.route('/api/v1.0/users', methods=['POST'])
def create_task():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'username': request.json['username'],
        'description': request.json['password'],
        'points': 0
    }
    users.append(user)
    return jsonify({'task': user}), 201
```

Before we build these all out, however, let's take a step back and connect this to a database.
==> Check out a full local db on app_local_db.py

## Connecting to A Database

I will use the following:

- [SQLAlchemy: a Python SQL toolkit](https://www.sqlalchemy.org/)
- [Marshmallow: deserialization library](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
- [Werkzeug: a Python library with great security functions](https://techmonger.github.io/4/secure-passwords-werkzeug/)

Marshmallow shemas allow our REST api to return values we retrieve from the database.

## How do I run this?

First time heroku app setup:

```
heroku login
heroku create my-app-rest-api
```

Any new changes:

```
git add .
git commit -m "my first server"
git push heroku master
```

First time postgres database setup:

```
heroku addons:add heroku-postgresql:hobby-dev
heroku run python
>>> from app import db
>>> db.create_all()
>>> exit()
```
