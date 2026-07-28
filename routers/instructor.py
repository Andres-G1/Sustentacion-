from flask import Blueprint, request, render_template, url_for, redirect, session
from models.models import Instructor

instructor_bp = Blueprint('instructor', __name__, url_prefix="/instructor")

@instructor_bp.route("/instructor")
def instructor():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if id_actual and role_actual == 'Instructor':
        instructor_data = Instructor.query.get(id_actual)
        if instructor_data:
            return render_template("module_I.html", user=instructor_data)

    return redirect(url_for("home"))