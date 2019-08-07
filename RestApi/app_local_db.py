from flask import Flask, jsonify, abort, make_response

app_local = Flask(__name__)

users = [
    {
        'username': 'helenamerk',
        'password': 'super_secret', 
        'points': 1738
    },
    {
        'username': 'player2',
        'password': 'more_secret', 
        'points': 1506
    },
]

@app_local.route('/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app_local.route('/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@app_local.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app_local.run(debug=True)