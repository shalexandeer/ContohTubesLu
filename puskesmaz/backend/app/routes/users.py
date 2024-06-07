from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.users import get_users, get_user_by_id, insert_user, update_user, delete_user
from app.utils import make_response

api = Blueprint('users', __name__)

@api.route("/api/users", methods=["GET"])
@jwt_required()
def api_get_users():
    users = get_users()
    return make_response(200, "Users retrieved successfully", users)

@api.route('/api/users/<user_id>', methods=['GET'])
@jwt_required()
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return make_response(200, "User retrieved successfully", user)
    else:
        return make_response(404, "User not found", {})

@api.route('/api/users/add', methods=['POST'])
@jwt_required()
def api_add_user():
    user = request.get_json()
    inserted_user = insert_user(user)
    if inserted_user:
        return make_response(201, "User added successfully", inserted_user)
    else:
        return make_response(400, "Error adding user", {})

@api.route('/api/users/update', methods=['PUT'])
@jwt_required()
def api_update_user():
    user = request.get_json()
    updated_user = update_user(user)
    if updated_user:
        return make_response(200, "User updated successfully", updated_user)
    else:
        return make_response(400, "Error updating user", {})

@api.route('/api/users/delete/<user_id>', methods=['DELETE'])
@jwt_required()
def api_delete_user(user_id):
    result = delete_user(user_id)
    if result["status"] == "User deleted successfully":
        return make_response(200, result["status"], {})
    else:
        return make_response(400, result["status"], {})
