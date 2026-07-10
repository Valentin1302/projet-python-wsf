from flask import Flask, request, jsonify
from functools import wraps
import json

app = Flask(__name__)

GLOBAL_API_KEY = "api-key-123"

def auth_wrapper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != GLOBAL_API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['POST'])
@auth_wrapper
def create_user():
    data = request.get_json()
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    users.append(user)
    
    with open('users.json', 'w') as f:
        json.dump(users, f)
    
    return jsonify(user), 201

@app.route('/users', methods=['GET'])
@auth_wrapper
def get_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
@auth_wrapper
def get_user(user_id):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if user_id <= len(users):
        user = users[user_id - 1]
        return jsonify(user), 200
    
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
@auth_wrapper
def update_user(user_id):
    data = request.get_json()
    
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if user_id <= len(users):
        user = users[user_id - 1]
        if 'first_name' in data:
            user['first_name'] = data['first_name']
        if 'last_name' in data:
            user['last_name'] = data['last_name']
        if 'email' in data:
            user['email'] = data['email']
        
        with open('users.json', 'w') as f:
            json.dump(users, f)
        
        return jsonify(user), 200
    
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
@auth_wrapper
def delete_user(user_id):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if user_id <= len(users):
        deleted = users.pop(user_id - 1)
        
        with open('users.json', 'w') as f:
            json.dump(users, f)
        
        return jsonify({"message": "User deleted"}), 200
    
    return jsonify({"error": "User not found"}), 404

@app.route('/blogs', methods=['POST'])
@auth_wrapper
def blog_articles():
    data = request.get_json()
    return jsonify(data), 201

@app.route('/blog/<post_id>', methods=['GET'])
@auth_wrapper
def blog_article(post_id):
    return f'Hello, World! {post_id}'

@app.route('/calculator', methods=['POST'])
@auth_wrapper
def calculator():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    return a * b
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)