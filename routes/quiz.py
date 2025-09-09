from flask import Blueprint, render_template, request, session, redirect
from utils.firebase_config import db

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/quiz/<curso_id>", methods=["GET", "POST"])
def quiz(curso_id):
    if "user_id" not in session:
        return redirect("/login")

    curso = db.collection("cursos").document(curso_id).get().to_dict()
    preguntas = curso.get("quiz", [])

    if request.method == "POST":
        puntaje = 0
        for i, pregunta in enumerate(preguntas):
            seleccion = request.form.get(f"pregunta{i}")
            if seleccion and int(seleccion) == pregunta["respuestaCorrecta"]:
                puntaje += 1

        # Guardar en el historial del usuario
        db.collection("usuarios").document(session["user_id"]).set({
            "progress": {
                curso_id: {"completado": True, "puntaje": puntaje}
            }
        }, merge=True)

        return redirect("/history")

    return render_template("quiz.html", curso=curso, preguntas=preguntas)
