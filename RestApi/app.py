from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/local-db'
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    points = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Username %r>' % self.username


# Routes

@app.route("/")
def hello():
    return "Hello World from api!"

@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    users = db.session.query(User)
    return jsonify({'users': users})


@app.route('/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.query(User).filter(User.id == user_id)

    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


# Save user to database and send to success page
@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    username = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check that username does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.username == username).count():
            reg = User(username, password)
            db.session.add(reg)
            db.session.commit()
            return jsonify({'user': reg})

    return jsonify({'error': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()