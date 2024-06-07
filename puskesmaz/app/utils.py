from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

def make_response(status, message, data):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response)

def hash_password(password):
    return generate_password_hash(password)

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
