from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users

coordinador_bp = Blueprint('coordinador', __name__, url_prefix="/coordinador")

@coordinador_bp.route("/coordinador")
def coordinador():
    id_actual = session.get('user_id') 
    if id_actual in users: 
        return render_template("module_C.html", users=users[id_actual]) 
    return redirect(url_for("home"))

@coordinador_bp.route("/coordinador_create_A", methods=["GET", "POST"])
def coordinador_create_A():
    if request.method == "POST":
        typeid = request.form.get('typeid')
        id = request.form.get('id')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        password = "1234"
        role = "Aprendiz"

        if id not in users:
            users[id] = {
                "typeid": typeid,
                "email": email,
                "name": name,
                "lastname": lastname,
                "password": password,
                "role": role
            }
            return redirect(url_for("coordinador.coordinador_create_A"))
        else:
            return render_template("C_Create_Aprendiz.html", error="Credencial existente")
            
    return render_template("C_Create_Aprendiz.html")

@coordinador_bp.route("/coordinador_alter_A", methods=["GET", "POST"])
def coordinador_alter_A():
    return