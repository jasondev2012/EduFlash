from flask import Blueprint, render_template, session, redirect
from utils.firebase_config import db

history_bp = Blueprint('history', __name__)

@history_bp.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    doc = db.collection("usuarios").document(session["user_id"]).get()
    data = doc.to_dict() or {}
    progress = data.get("progress", {})

    return render_template("history.html", progress=progress)
