from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users

aprendiz_bp = Blueprint('aprendiz', __name__, url_prefix="/aprendiz")

@aprendiz_bp.route("/aprendiz")
def aprendiz():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("module_A.html", users=users[id_actual])
    return redirect(url_for("home"))