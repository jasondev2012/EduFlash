from flask import Blueprint, render_template, session, redirect
from models.course import Course

courses_bp = Blueprint('courses', __name__)

@courses_bp.route("/courses")
def list_courses():
    # if "user_id" not in session:
    #     return redirect("/login")

    cursos = [] # Course.all()
    return render_template("business/courses.html", cursos=cursos)
