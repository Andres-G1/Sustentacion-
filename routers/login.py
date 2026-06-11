from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users

user_bp = Blueprint('users', __name__, url_prefix="/users")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        typeid = request.form.get('typeid')
        id = request.form.get('id')
        password = request.form.get('password')

        if id in users and users[id]['password'] == password and users[id]['typeid'] == typeid:
            session['user_id'] = id
            match users[id]["role"]:
                case "Coordinador":
                    return redirect(url_for("module.coordinador"))
                case "Instructor":
                    return redirect(url_for("module.instructor"))
                case "Aprendiz":
                    return redirect(url_for("module.aprendiz"))
            
    return render_template("login.html", error="Invalid credentials") 