import requests
from flask import Blueprint, render_template, request, jsonify, session
from models.user import User
from utils.firebase_config import auth
import os

from utils.response import error_response, success_response

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/logout")
def logout():
    """Cerrar sesión del usuario"""
    session.pop("user", None) 
    return render_template("index.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return error_response("Faltan credenciales", status=400)
    print(FIREBASE_API_KEY)
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload)
        data = response.json()

        if "idToken" in data:
            return success_response(
                message="Login exitoso",
                data={
                    "uid": data["localId"],
                    "email": data["email"],
                    "idToken": data["idToken"],
                    "refreshToken": data["refreshToken"]
                }
            )

        return error_response("Credenciales inválidas", error=data.get("error", {}), status=401)

    except Exception as e:
        return error_response("Error en el login", error=str(e), status=500)



@auth_bp.route("/registro", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    nombres = request.form.get("nombres")
    apellidos = request.form.get("apellidos")

    if not email or not password or not nombres or not apellidos:
        return error_response("Faltan datos del registro", status=400)

    try:
        user_record = auth.create_user(email=email, password=password)
        User.create(uid=user_record.uid, email=email, nombres=nombres, apellidos=apellidos)
        return success_response(
            message="Usuario registrado con éxito",
            data={"uid": user_record.uid, "email": email},
            status=201
        )
    except Exception as e:
        return error_response("Error al registrar usuario", error=str(e), status=400)
