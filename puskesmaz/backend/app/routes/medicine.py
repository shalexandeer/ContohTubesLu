from flask import Blueprint, request
from app.models.medicine import get_medicines, get_medicine_by_id, insert_medicine, update_medicine, delete_medicine
from app.utils import make_response
from flask_jwt_extended import jwt_required

api = Blueprint('medicine', __name__)

@api.route("/api/medicines", methods=["GET"])
@jwt_required()
def api_get_medicines():
    medicines = get_medicines()
    return make_response(200, "Medicines retrieved successfully", medicines)

@api.route('/api/medicines/<medicine_id>', methods=['GET'])
@jwt_required()
def api_get_medicine(medicine_id):
    medicine = get_medicine_by_id(medicine_id)
    if medicine:
        return make_response(200, "Medicine retrieved successfully", medicine)
    else:
        return make_response(404, "Medicine not found", {})

@api.route('/api/medicines/add', methods=['POST'])
@jwt_required()
def api_add_medicine():
    medicine = request.get_json()
    inserted_medicine = insert_medicine(medicine)
    if inserted_medicine:
        return make_response(201, "Medicine added successfully", inserted_medicine)
    else:
        return make_response(400, "Error adding medicine", {})

@api.route('/api/medicines/update', methods=['PUT'])
@jwt_required()
def api_update_medicine():
    medicine = request.get_json()
    updated_medicine = update_medicine(medicine)
    if updated_medicine:
        return make_response(200, "Medicine updated successfully", updated_medicine)
    else:
        return make_response(400, "Error updating medicine", {})

@api.route('/api/medicines/delete/<medicine_id>', methods=['DELETE'])
@jwt_required()
def api_delete_medicine(medicine_id):
    result = delete_medicine(medicine_id)
    if result["status"] == "Medicine deleted successfully":
        return make_response(200, result["status"], {})
    else:
        return make_response(400, result["status"], {})
