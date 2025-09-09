from flask import jsonify

def success_response(message="Operación exitosa", data=None, status=200):
    response = {
        "success": True,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status


def error_response(message="Error en la operación", error=None, status=400):
    response = {
        "success": False,
        "message": message,
    }
    if error is not None:
        response["error"] = error
    return jsonify(response), status
