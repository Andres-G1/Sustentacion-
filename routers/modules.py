from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users

module_bp = Blueprint('module', __name__, url_prefix="/module")

@module_bp.route("/coordinador")
def coordinador():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("module_C.html", users=users[id_actual])
    return redirect(url_for("home"))

@module_bp.route("/instructor")
def instructor():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("module_I.html", users=users[id_actual])
    return redirect(url_for("home"))

@module_bp.route("/aprendiz")
def aprendiz():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("module_A.html", users=users[id_actual])
    return redirect(url_for("home"))

@module_bp.route("/password")
def password():
    return render_template("Password.html")