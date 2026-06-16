from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users


instructor_bp = Blueprint('instructor', __name__, url_prefix="/instructor")

@instructor_bp.route("/instructor")
def instructor():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("module_I.html", users=users[id_actual])
    return redirect(url_for("home"))