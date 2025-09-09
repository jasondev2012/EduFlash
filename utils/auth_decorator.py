# src/utils/auth_decorator.py
from functools import wraps
from flask import request, jsonify
import requests
import os
from firebase_admin import firestore

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
db = firestore.client()

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "message": "Token requerido"}), 401

        id_token = auth_header.split(" ")[1]

        # 🔹 Verificar el token con Firebase
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
        res = requests.post(url, json={"idToken": id_token})
        firebase_response = res.json()

        if "error" in firebase_response:
            return jsonify({
                "success": False,
                "message": firebase_response["error"]["message"]
            }), 401

        user_data = firebase_response["users"][0]
        uid = user_data.get("localId")
        email = user_data.get("email")

        # 🔹 Buscar datos adicionales en Firestore
        user_ref = db.collection("usuarios").document(uid).get()
        nombres = None
        apellidos = None
        if user_ref.exists:
            user_info = user_ref.to_dict()
            nombres = user_info.get("nombres")
            apellidos = user_info.get("apellidos")

        # 🔹 Solo lo básico que necesita tu frontend
        filtered_user = {
            "uid": uid,
            "email": email,
            "nombres": nombres,
            "apellidos": apellidos
        }

        request.user = filtered_user  # 👈 Inyectamos solo lo necesario

        return f(*args, **kwargs)
    return decorated_function
