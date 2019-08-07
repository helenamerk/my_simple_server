from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash


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
    email = db.Column(db.String(120), index=True, unique=True)
    #password = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer)

    

    def __repr__(self):
        return '<Username %r>' % self.username

    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'points')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

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
    user = User.query.get(user_id)
    return user_schema.jsonify(user)

# endpoint to update user
@app.route("/api/v1.0/users/<int:user_id>", methods=["PUT"])
def user_update(user_id):
    u = User.query.get(user_id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if u.check_password(password):
        u.set_password(password)
        u.username = username
        u.email = email

    db.session.commit()
    return user_schema.jsonify(u)

# Save user to database and send to success page
@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    username = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check that username does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.username == username).count():
            u = User(username, email)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            #return jsonify({'user': u})
            return 'Success'

    return jsonify({'error': True})

# endpoint to delete user
@app.route("/api/v1.0/users/<int:user_id>", methods=["DELETE"])
def user_delete(user_id):
    u = User.query.get(user_id)
    db.session.delete(u)
    db.session.commit()

    return user_schema.jsonify(u)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()