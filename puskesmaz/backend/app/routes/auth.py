from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.models.users import insert_user, get_user_by_email
from app.utils import make_response, check_password

api = Blueprint('auth', __name__)

@api.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if get_user_by_email(data['email']):
        return make_response(400, "User already exists", {})
    new_user = insert_user(data)
    if new_user:
        return make_response(201, "User registered successfully", new_user)
    else:
        return make_response(400, "Error registering user", {})

@api.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user_by_email(data['email'])
    if user and check_password(user['password'], data['password']):
        access_token = create_access_token(identity={'email': user['email']})
        return make_response(200, "Login successful", {'access_token': access_token})
    else:
        return make_response(401, "Invalid credentials", {})
