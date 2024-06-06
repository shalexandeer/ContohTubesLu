from flask import jsonify

def make_response(status, message, data):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response)
