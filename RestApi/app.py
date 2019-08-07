from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_marshmallow import Marshmallow


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/local-db'
heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

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

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'points')

# Routes
@app.route("/")
def hello():
    return "Hello World from api!"

@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route('/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id) #db.session.query(User).filter(User.id == user_id) 
    return user_schema.jsonify(user)

# endpoint to update user
@app.route("/api/v1.0/users/<int:user_id>", methods=["PUT"])
def user_update(user_id):
    user = User.query.get(user_id)
    username = request.json['username']
    password = request.json['password']

    user.password = password
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)

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
            #return jsonify({'user': reg})
            return 'Success'

    return jsonify({'error': True})

# endpoint to delete user
@app.route("/api/v1.0/users/<int:user_id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()