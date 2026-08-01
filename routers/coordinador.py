from flask import Blueprint, request, render_template, url_for, redirect, session
from models.models import Administrador, Aprendiz, Instructor, Fichas, Carrera
from werkzeug.security import generate_password_hash
from database import db

coordinador_bp = Blueprint('coordinador', __name__, url_prefix="/coordinador")

@coordinador_bp.route("/coordinador")
def coordinador():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if id_actual and role_actual == 'Coordinador':
        coordinador_data = Administrador.query.get(id_actual)
        if coordinador_data:
            return render_template("module_C.html", user=coordinador_data)

    return redirect(url_for("home"))

"============== MODULES CONFIG ==============="

@coordinador_bp.route("/module_aprendiz_config")
def module_aprendiz_config():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if id_actual and role_actual == 'Coordinador':
        coordinador_data = Administrador.query.get(id_actual)
        if coordinador_data:
            lista_aprendiz = Aprendiz.query.all()
            return render_template("Aprendiz_config.html", users=lista_aprendiz, user=coordinador_data)

    return redirect(url_for("home"))

@coordinador_bp.route("/module_instructor_config")
def module_instructor_config():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if id_actual and role_actual == 'Coordinador':
        coordinador_data = Administrador.query.get(id_actual)
        if coordinador_data:
            lista_instructor = Instructor.query.all()
            return render_template("Instructor_config.html", users=lista_instructor, user=coordinador_data)

    return redirect(url_for("home"))

@coordinador_bp.route("/module_coordinador_config")
def module_coordinador_config():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if id_actual and role_actual == 'Coordinador':
        coordinador_data = Administrador.query.get(id_actual)
        if coordinador_data:
            listar_coordinador = Administrador.query.all()
            return render_template("Coordinador_config.html", users=listar_coordinador, user=coordinador_data)

    return redirect(url_for("home"))

"============== APREDIZ CREATE, DELETE, MODIFY =============="

@coordinador_bp.route("/coordinador_create_A", methods=["GET", "POST"])
def coordinador_create_A():
    
    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))

    Avilable_career = Carrera.query.all()
    Select_career = request.args.get("career") or request.form.get("career")
    Tokens_avilable = Fichas.query.filter_by(Id_Car=Select_career).all() if Select_career else []

    if request.method == "POST":
        typeid = request.form.get('typeid')
        num_id = request.form.get('id')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        token_id = request.form.get('token')
        password = "1234"
        
        aprendiz_existing = Aprendiz.query.filter(
            (Aprendiz.Num_ide_Apr == num_id) | (Aprendiz.Cor_Apr == email)
        ).first()

        if aprendiz_existing is None:
            new_aprendiz = Aprendiz(
                Nom_Apr=name,
                Ape_Apr=lastname,
                Tip_ide_Apr=typeid,
                Num_ide_Apr=num_id,
                Cor_Apr=email,
                Con_Apr=generate_password_hash(password),
                Id_Fic=token_id
            )
            db.session.add(new_aprendiz)
            db.session.commit()
            return redirect(url_for("coordinador.module_aprendiz_config"))
        else:
            return render_template(
                "C_Create_Aprendiz.html",
                error="Credencial existente",
                career=Avilable_career,
                token=Tokens_avilable,
                careers_selected=Select_career,
                user=coordinador_data
            )

    return render_template(
        "C_Create_Aprendiz.html",
        career = Avilable_career,
        token=Tokens_avilable,
        careers_selected=Select_career,
        user=coordinador_data
    )

@coordinador_bp.route("/coordinador_alter_A/<id>", methods=["GET", "POST"])
def coordinador_alter_A(id):

    id_actual = session.get('user_id')

    user_id = str(id)

    if user_id not in users or users[user_id].get("role") != "Aprendiz":
        return redirect(url_for("coordinador.module_aprendiz_config"))

    if request.method == "POST" and id_actual in users:

        users[user_id]['typeid'] = request.form.get('typeid')
        users[user_id]['email'] = request.form.get('email')
        users[user_id]['name'] = request.form.get('name')
        users[user_id]['lastname'] = request.form.get('lastname')
        users[user_id]['password'] = request.form.get('password')
        users[user_id]['token'] = request.form.get('token')

        return redirect(url_for("coordinador.module_aprendiz_config"))

    usuario = users.get(user_id)

    carrera_actual = None
    for nombre_carrera, lista_tokens in token.items():
        if usuario.get("token") in lista_tokens:
            carrera_actual = nombre_carrera
            break
    fichas_disponibles = token.get(carrera_actual, [])

    return render_template(
        "C_Alter_Aprendiz.html",
        id=user_id,
        usuario=usuario,
        user=users[id_actual],
        carrera_actual=carrera_actual,
        fichas_disponibles=fichas_disponibles
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
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))


    if request.method == "POST":
        typeid = request.form.get('typeid')
        num_id = request.form.get('id')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        password = "1234"
        
        Instructor_existing = Instructor.query.filter(
            (Instructor.Num_ide_Ins == num_id) | (Instructor.Cor_Ins == email)
        ).first()
        
        if Instructor_existing is None:
            new_aprendiz = Instructor(
                Nom_Ins=name,
                Ape_Ins=lastname,
                Tip_ide_Ins=typeid,
                Num_ide_Ins=num_id,
                Cor_Ins=email,
                Con_Ins=generate_password_hash(password),
                )
            db.session.add(new_aprendiz)
            db.session.commit()
            return redirect(url_for("coordinador.module_instructor_config"))
                
        else:
            return render_template(
                "C_Create_Instructor.html",
                error="Credencial existente",
                user=coordinador_data
            )

    return render_template(
        "C_Create_Instructor.html",
        user=coordinador_data
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

    user_id = str(id)
    if request.method == "POST":
        if user_id in users and users[user_id].get("role") == "Instructor" and id_actual in users:
            users.pop(user_id)
            return redirect(url_for("coordinador.module_instructor_config"))
        return render_template(
            "C_Delete_Instructor.html",
            error="Instructor no encontrado.",
            id=id,
            usuario=None
        )

    usuario = users.get(user_id)
    return render_template(
        "C_Delete_Instructor.html",
        id=id,
        usuario=usuario,
        user=users[id_actual]
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

    user_id = str(id)
    if request.method == "POST":
        if user_id in users and users[user_id].get("role") == "Coordinador" and id_actual in users:
            users.pop(user_id)
            return redirect(url_for("coordinador.module_coordinador_config"))
        return render_template(
            "C_Delete_Coordinador.html",
            error="Coordinador no encontrado.",
            id=id,
            usuario=None
        )

    usuario = users.get(user_id)
    return render_template(
        "C_Delete_Coordinador.html",
        id=id,
        usuario=usuario,
        user = users[id_actual]
    )