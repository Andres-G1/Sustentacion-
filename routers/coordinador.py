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

@coordinador_bp.route("/coordinador_alter_A/<Id_Apr>", methods=["GET", "POST"])
def coordinador_alter_A(Id_Apr):
    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
    
    users = Aprendiz.query.get(Id_Apr)
    if not users:
        return "Aprendiz no encontrado", 404
    
    errors = {}
    
    if request.method == "POST":
        typeid = request.form.get('typeid', '').strip()
        email = request.form.get('email', '').strip()
        name = request.form.get('name', '').strip()
        lastname = request.form.get('lastname', '').strip()
        password = request.form.get('password', '').strip()
        
        if not typeid:
            errors['typeid'] = "El tipo de identificación es obligatorio."
        if not email:
            errors['email'] = "El correo es obligatorio."
        if not name:
            errors['name'] = "El nombre es obligatorio."
        if not lastname:
            errors['lastname'] = "El apellido es obligatorio."
        
        if not errors:
            users.Tip_ide_Apr = typeid
            users.Cor_Apr = email
            users.Nom_Apr = name
            users.Ape_Apr = lastname
            
            if password:
                users.Con_Apr = generate_password_hash(password)
            
            db.session.commit()
            return redirect(url_for("coordinador.module_aprendiz_config"))
    
    Current_Career = "No asignada"
    Avilable_Tokens = []
    
    token_user = Fichas.query.filter_by(Id_Fic=users.Id_Fic).first()
    if token_user:
        carrera_obj = Carrera.query.get(token_user.Id_Car)
        if carrera_obj:
            Current_Career = carrera_obj.Nom_Car
        
        Tokens_db = Fichas.query.filter_by(Id_Car=token_user.Id_Car).all()
        Avilable_Tokens = [f.Num_Fic for f in Tokens_db]
    
    return render_template(
        'C_Alter_Aprendiz.html',
        id=id_actual,
        usuario=users,
        user=coordinador_data,
        carrera_actual=Current_Career,
        Avilable_Tokens=Avilable_Tokens,
        errors=errors
    )


@coordinador_bp.route("/coordinador_delete_A/<int:Id_Apr>", methods=["GET", "POST"])
def coordinador_delete_A(Id_Apr):

    id_actual = session.get('user_id')
    role_actual = session.get('role')
        
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
        
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
        
    aprendiz = Aprendiz.query.get(Id_Apr)
    if not aprendiz:
        return "Aprendiz no encontrado", 404

    if request.method == "POST":
            db.session.delete(aprendiz)  
            db.session.commit() 
            return redirect(url_for("coordinador.module_aprendiz_config"))

    return render_template(
        "C_Delete_Aprendiz.html",
        id=Id_Apr,
        usuario=aprendiz,    
        user=coordinador_data     
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
            new_instructor = Instructor(
                Nom_Ins=name,
                Ape_Ins=lastname,
                Tip_ide_Ins=typeid,
                Num_ide_Ins=num_id,
                Cor_Ins=email,
                Con_Ins=generate_password_hash(password),
                )
            db.session.add(new_instructor)
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

@coordinador_bp.route("/coordinador_alter_I/<Id_Ins>", methods=["GET", "POST"])
def coordinador_alter_I(Id_Ins):

    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
    
    users = Instructor.query.get(Id_Ins)
    if not users:
        return "Instructor no encontrado", 404

    if request.method == "POST":

        users.Tip_ide_Ins = request.form.get('typeid')
        users.Cor_Ins = request.form.get('email')
        users.Nom_Ins = request.form.get('name')
        users.Ape_Ins = request.form.get('lastname')
        password = request.form.get('password')
        if password and password.strip():
            users.Con_Ins = generate_password_hash(password)
        
        db.session.commit()

        return redirect(url_for("coordinador.module_instructor_config"))

    return render_template(
        'C_Alter_Instructor.html', 
        id=id_actual, 
        usuario=users, 
        user=coordinador_data, 
    )

@coordinador_bp.route("/coordinador_delete_I/<int:Id_Ins>", methods=["GET", "POST"])
def coordinador_delete_I(Id_Ins):
    
    id_actual = session.get('user_id')
    role_actual = session.get('role')
        
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
        
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
        
    instructor = Instructor.query.get(Id_Ins)
    if not instructor:
        return "Instructor no encontrado", 404

    if request.method == "POST":
            db.session.delete(instructor)  
            db.session.commit() 
            return redirect(url_for("coordinador.module_instructor_config"))

    return render_template(
        "C_Delete_Instructor.html",
        id=Id_Ins,
        usuario=instructor,    
        user=coordinador_data     
    )

"============== COORDINADOR CREATE, DELETE, MODIFY =============="

@coordinador_bp.route("/coordinador_create_C", methods=["GET", "POST"])
def coordinador_create_C():

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


        Administrador_existing = Administrador.query.filter(
            (Administrador.Num_ide_Adm == num_id) | (Administrador.Cor_Adm == email)
        ).first()
        
        if Administrador_existing is None:
            new_coordinador = Administrador(
                Nom_Adm=name,
                Ape_Adm=lastname,
                Tip_ide_Adm=typeid,
                Num_ide_Adm=num_id,
                Cor_Adm=email,
                Con_Adm=generate_password_hash(password),
                )
            db.session.add(new_coordinador)
            db.session.commit()
            return redirect(url_for("coordinador.module_coordinador_config"))
                
        else:
            return render_template(
                "C_Create_Coordinador.html",
                error="Credencial existente",
                user=coordinador_data
            )

    return render_template(
        "C_Create_Coordinador.html",
        user=coordinador_data
    )

@coordinador_bp.route("/coordinador_alter_C/<Id_Adm>", methods=["GET", "POST"])
def coordinador_alter_C(Id_Adm):

    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
    
    users = Administrador.query.get(Id_Adm)
    if not users:
        return "Coordinador no encontrado", 404

    if request.method == "POST":

        users.Tip_ide_Adm = request.form.get('typeid')
        users.Cor_Adm = request.form.get('email')
        users.Nom_Adm = request.form.get('name')
        users.Ape_Adm = request.form.get('lastname')
        
        password = request.form.get('password')
        if password and password.strip():
            users.Con_Adm = generate_password_hash(password)
        
        db.session.commit()

        return redirect(url_for("coordinador.module_coordinador_config"))

    return render_template(
        'C_Alter_Coordinador.html', 
        id=id_actual, 
        usuario=users, 
        user=coordinador_data, 
    )

@coordinador_bp.route("/coordinador_delete_C/<int:Id_Adm>", methods=["GET", "POST"])
def coordinador_delete_C(Id_Adm):

    id_actual = session.get('user_id')
    role_actual = session.get('role')
        
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
        
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
        
    administrador = Administrador.query.get(Id_Adm)
    if not administrador:
        return "Instructor no encontrado", 404

    if request.method == "POST":
            db.session.delete(administrador)  
            db.session.commit() 
            return redirect(url_for("coordinador.module_coordinador_config"))

    return render_template(
        "C_Delete_Coordinador.html",
        id=Id_Adm,
        usuario=administrador,    
        user=coordinador_data     
    )