from flask import Blueprint, request, jsonify
from models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Check if the user already exists
    existing_user = Users.query.filter_by(username=username).first()
    
    if existing_user:
        return jsonify(message="User already exists"), 400  # Return 400 Bad Request
    
    # Hash the password
    hashed_password = generate_password_hash(password)
    
    # Create the new user
    new_user = Users(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = Users.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401
