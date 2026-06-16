from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users, attendance

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
                    return redirect(url_for("coordinador.coordinador"))
                case "Instructor":
                    return redirect(url_for("instructor.instructor"))
                case "Aprendiz":
                    return redirect(url_for("aprendiz.aprendiz"))
            
    return render_template("login.html", error="Invalid credentials")

@user_bp.route("/password")
def password():
    return render_template("Password.html") 