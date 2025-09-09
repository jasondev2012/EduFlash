from flask import Blueprint, jsonify, request, session
from utils.auth_decorator import require_auth
from utils.response import success_response

seguridad_bp = Blueprint("seguridad", __name__)

@seguridad_bp.route("/perfil", methods=["GET"])
@require_auth
def perfil():
    user = request.user  # <- viene del decorador
    session["user"] = {
        "uid": user["uid"],
        "email": user["email"],
        "nombres": user["nombres"]
    }
    return success_response(
        message="Login exitoso",
        data=user
    )
