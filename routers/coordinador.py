from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users, token, career

coordinador_bp = Blueprint('coordinador', __name__, url_prefix="/coordinador")

@coordinador_bp.route("/coordinador")
def coordinador():
    id_actual = session.get('user_id') 
    if id_actual in users: 
        return render_template("module_C.html", users=users[id_actual]) 
    return redirect(url_for("home"))

@coordinador_bp.route("/coordinador_create_A", methods=["GET", "POST"])
def coordinador_create_A():

    career_avaliable = career["career"]
    selected_career = request.args.get("career") or request.form.get("career")
    fichas_avaliable = token.get(selected_career, [])

    if request.method == "POST":
        typeid = request.form.get('typeid')
        id = request.form.get('id')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        career_form = request.form.get('career')
        token_form = request.form.get('token')
        password = "1234"
        role = "Aprendiz"

        if id not in users:
            users[id] = {
                "typeid": typeid,
                "email": email,
                "name": name,
                "lastname": lastname,
                "career": career_form,
                "token": token_form,
                "password": password,
                "role": role
            }
            return redirect(url_for("coordinador.coordinador_create_A"))
        else:
            return render_template(
                "C_Create_Aprendiz.html",
                error="Credencial existente",
                carreras=career_avaliable,
                fichas=fichas_avaliable,
                carrera_seleccionada=selected_career
            )

    return render_template(
        "C_Create_Aprendiz.html",
        carreras=career_avaliable,
        fichas=fichas_avaliable,
        carrera_seleccionada=selected_career
    )
@coordinador_bp.route("/coordinador_alter_A", methods=["GET", "POST"])
def coordinador_alter_A():
    if request.method == "POST":
        if users[id] == users[id]:
            typeid = request.form.get('typeid')
            email = request.form.get('email')
            name = request.form.get('name')
            lastname = request.form.get('lastname')
            password = request.form.get('password')
            role = "Aprendiz"

    return render_template("C_Alter_Aprendiz.html")