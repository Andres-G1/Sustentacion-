from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users, token, career

coordinador_bp = Blueprint('coordinador', __name__, url_prefix="/coordinador")

@coordinador_bp.route("/coordinador")
def coordinador():
    id_actual = session.get('user_id') 
    if id_actual in users: 
        return render_template("module_C.html", users=users[id_actual]) 
    return redirect(url_for("home"))

"============== MODULES CONFIG ==============="

@coordinador_bp.route("/module_aprendiz_config")
def module_aprendiz_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Aprendiz_config.html", users=users, user=users[id_actual])
    return redirect(url_for("home"))

@coordinador_bp.route("/module_instructor_config")
def module_instructor_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Instructor_config.html", users=users, user=users[id_actual])
    return redirect(url_for("home"))

@coordinador_bp.route("/module_coordinador_config")
def module_coordinador_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Coordinador_config.html", users=users, user=users[id_actual])
    return redirect(url_for("home"))

"============== APREDIZ CREATE, DELETE, MODIFY =============="

@coordinador_bp.route("/coordinador_create_A", methods=["GET", "POST"])
def coordinador_create_A():
       
    career_avaliable = career["career"]
    selected_career = request.args.get("career") or request.form.get("career")
    fichas_avaliable = token.get(selected_career, [])
    id_actual = session.get('user_id')

    if request.method == "POST" and id_actual in users:
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
            return redirect(url_for("coordinador.module_aprendiz_config"))
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
        carrera_seleccionada=selected_career,
        user=users[id_actual]
    )

@coordinador_bp.route("/coordinador_alter_A/<id>", methods=["GET", "POST"])
def coordinador_alter_A(id):

    id_actual = session.get('user_id')
    
    user_id = str(id)
    
    if user_id not in users or users[user_id].get("role") != "Aprendiz":
        return redirect(url_for("coordinador.module_aprendiz_config"))

    if request.method == "POST" and id_actual in users :

        users[user_id]['typeid'] = request.form.get('typeid')
        users[user_id]['email'] = request.form.get('email')
        users[user_id]['name'] = request.form.get('name')
        users[user_id]['lastname'] = request.form.get('lastname')
        users[user_id]['password'] = request.form.get('password')
        
        return redirect(url_for("coordinador.module_aprendiz_config"))

    usuario = users.get(user_id)
    return render_template(
        "C_Alter_Aprendiz.html",
        id=user_id,
        usuario=usuario,
        user = users[id_actual]
    )

@coordinador_bp.route("/coordinador_delete_A/<int:id>", methods=["GET", "POST"])
def coordinador_delete_A(id):
    id_actual = session.get('user_id')

    user_id = str(id)
    if request.method == "POST":
        if user_id in users and users[user_id].get("role") == "Aprendiz" and id_actual in users :
            users.pop(user_id)
            return redirect(url_for("coordinador.module_aprendiz_config"))
        return render_template(
            "C_Delete_Aprendiz.html",
            error="Aprendiz no encontrado.",
            id=id,
            usuario=None
        )

    usuario = users.get(user_id)
    return render_template(
        "C_Delete_Aprendiz.html",
        id=id,
        usuario=usuario,
        user = users[id_actual]
    )

"============== INSTRUCTOR CREATE, DELETE, MODIFY =============="

@coordinador_bp.route("/coordinador_create_I", methods=["GET", "POST"])
def coordinador_create_I():

    id_actual = session.get('user_id')

    if request.method == "POST" and id_actual in users:
        typeid = request.form.get('typeid')
        id = request.form.get('id')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        password = "1234"
        role = "Instructor"

        if id not in users:
            users[id] = {
                "typeid": typeid,
                "email": email,
                "name": name,
                "lastname": lastname,
                "password": password,
                "role": role
            }
            return redirect(url_for("coordinador.module_instructor_config"))
        else:
            return render_template(
                "C_Create_Instructor.html",
                error="Credencial existente",
            )

    return render_template(
        "C_Create_Instructor.html",
        user=users[id_actual]
    )

@coordinador_bp.route("/coordinador_alter_I/<id>", methods=["GET", "POST"])
def coordinador_alter_I(id):

    id_actual = session.get('user_id')
    
    user_id = str(id)
    
    if user_id not in users or users[user_id].get("role") != "Instructor":
        return redirect(url_for("coordinador.module_instructor_config"))

    if request.method == "POST" and id_actual in users :

        users[user_id]['typeid'] = request.form.get('typeid')
        users[user_id]['email'] = request.form.get('email')
        users[user_id]['name'] = request.form.get('name')
        users[user_id]['lastname'] = request.form.get('lastname')
        users[user_id]['password'] = request.form.get('password')
        
        return redirect(url_for("coordinador.module_instructor_config"))

    usuario = users.get(user_id)
    return render_template(
        "C_Alter_Instructor.html",
        id=user_id,
        usuario=usuario,
        user = users[id_actual]
    )

@coordinador_bp.route("/coordinador_delete_I/<int:id>", methods=["GET", "POST"])
def coordinador_delete_I(id):
    id_actual = session.get('user_id')
    if id_actual not in users:
        return redirect(url_for("home"))

    user_id = str(id)
    if request.method == "POST":
        if user_id in users and users[user_id].get("role") == "Instructor":
            users.pop(user_id)
            return redirect(url_for("coordinador.module_instructor_config"))
        return render_template(
            "C_Delete_Instructor.html",
            error="Aprendiz no encontrado.",
            id=id,
            usuario=None
        )

    usuario = users.get(user_id)
    return render_template(
        "C_Delete_Instructor.html",
        id=id,
        usuario=usuario
    )

"============== COORDINADOR CREATE, DELETE, MODIFY =============="

@coordinador_bp.route("/coordinador_create_C", methods=["GET", "POST"])
def coordinador_create_C():

    id_actual = session.get('user_id')

    if request.method == "POST" and id_actual in users:
        typeid = request.form.get('typeid')
        id = request.form.get('id')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        password = "1234"
        role = "Coordinador"

        if id not in users:
            users[id] = {
                "typeid": typeid,
                "email": email,
                "name": name,
                "lastname": lastname,
                "password": password,
                "role": role
            }
            return redirect(url_for("coordinador.module_coordinador_config"))
        else:
            return render_template(
                "C_Create_Coordinador.html",
                error="Credencial existente",
            )

    return render_template(
        "C_Create_Coordinador.html",
        user=users[id_actual]
    )

@coordinador_bp.route("/coordinador_alter_C/<id>", methods=["GET", "POST"])
def coordinador_alter_C(id):

    id_actual = session.get('user_id')
    
    user_id = str(id)
    
    if user_id not in users or users[user_id].get("role") != "Coordinador":
        return redirect(url_for("coordinador.module_coordinador_config"))

    if request.method == "POST" and id_actual in users :

        users[user_id]['typeid'] = request.form.get('typeid')
        users[user_id]['email'] = request.form.get('email')
        users[user_id]['name'] = request.form.get('name')
        users[user_id]['lastname'] = request.form.get('lastname')
        users[user_id]['password'] = request.form.get('password')
        
        return redirect(url_for("coordinador.module_coordinador_config"))

    usuario = users.get(user_id)
    return render_template(
        "C_Alter_Coordinador.html",
        id=user_id,
        usuario=usuario,
        user = users[id_actual]
    )

@coordinador_bp.route("/coordinador_delete_C/<int:id>", methods=["GET", "POST"])
def coordinador_delete_C(id):
    id_actual = session.get('user_id')
    if id_actual not in users:
        return redirect(url_for("home"))

    user_id = str(id)
    if request.method == "POST":
        if user_id in users and users[user_id].get("role") == "Instructor":
            users.pop(user_id)
            return redirect(url_for("coordinador.module_coordinador_config"))
        return render_template(
            "C_Delete_Coordinador.html",
            error="Aprendiz no encontrado.",
            id=id,
            usuario=None
        )

    usuario = users.get(user_id)
    return render_template(
        "C_Delete_Coordinador.html",
        id=id,
        usuario=usuario
    )