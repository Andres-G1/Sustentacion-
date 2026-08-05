from flask import Blueprint, request, render_template, url_for, redirect, session
from models.models import Aprendiz, Administrador, Carrera, Fichas
from database import db

token_bp = Blueprint('token', __name__, url_prefix="/token")

@token_bp.route("/module_token_config")
def module_token_config():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))

    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))

    career_list = Carrera.query.all()

    return render_template(
        "Token_config.html", 
        user=coordinador_data, 
        token=career_list
    )

@token_bp.route("/Create_token", methods=["GET", "POST"])
def Create_token():
    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))

    career_avaliable = Carrera.query.all()

    if request.method == 'POST':
        id_carrera = request.form.get('career')
        numero_ficha = request.form.get('token')
        fecha_inicio = request.form.get('fec_inicio')
        fecha_fin = request.form.get('fec_fin')
        jornada = request.form.get('jornada')

        if not all([id_carrera, numero_ficha, fecha_inicio, fecha_fin, jornada]):
            return render_template(
                "C_Create_Token.html", 
                career_avaliable=career_avaliable, 
                user=coordinador_data, 
                error="Todos los campos son obligatorios."
            )

        token_existe = Fichas.query.filter_by(Num_Fic=numero_ficha).first()

        if not token_existe:

            nueva_ficha = Fichas(
                Id_Car=int(id_carrera),
                Num_Fic=int(numero_ficha),
                Fec_inicio_Fic=fecha_inicio, 
                Fec_Fin_Fic=fecha_fin,
                Jor_Fic=jornada
            )
            
            db.session.add(nueva_ficha)
            db.session.commit()          
            return redirect(url_for("token.module_token_config"))
        else:
            return render_template(
                "C_Create_Token.html", 
                career_avaliable=career_avaliable, 
                user=coordinador_data, 
                error="El número de ficha ya se encuentra registrado."
            )
        
    return render_template(
        "C_Create_Token.html",
        career_avaliable=career_avaliable,
        user=coordinador_data
    )

@token_bp.route("/Alter_token/<int:career>/<int:old_token>", methods=["GET", "POST"])
def Alter_token(career, old_token):
    
    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))
        
    carrera_obj = Carrera.query.get(career)
    ficha_obj = Fichas.query.filter_by(Id_Car=career, Num_Fic=old_token).first()
   
    if not carrera_obj or not ficha_obj:
        return redirect(url_for("token.module_token_config"))
    
    career_avaliable = Carrera.query.all()
 
    if request.method == "POST":
        id_carrera_nueva = request.form.get('career')
        nuevo_numero_ficha = request.form.get('token')
        nueva_fecha_inicio = request.form.get('fec_inicio')
        nueva_fecha_fin = request.form.get('fec_fin')
        nueva_jornada = request.form.get('jornada')
    
        if not all([id_carrera_nueva, nuevo_numero_ficha, nueva_fecha_inicio, nueva_fecha_fin, nueva_jornada]):
            return render_template(
                "C_Alter_Token.html",
                carrera_actual=carrera_obj,
                ficha=ficha_obj,
                career_avaliable=career_avaliable,
                user=coordinador_data,
                error="Todos los campos son obligatorios"
            )
            
        nuevo_numero_ficha = int(nuevo_numero_ficha)
        id_carrera_nueva = int(id_carrera_nueva)

        if nuevo_numero_ficha != old_token:
            token_duplicado = Fichas.query.filter_by(Num_Fic=nuevo_numero_ficha).first()
            if token_duplicado:
                return render_template(
                    "C_Alter_Token.html",
                    carrera_actual=carrera_obj,
                    ficha=ficha_obj,
                    career_avaliable=career_avaliable,
                    user=coordinador_data,
                    error="El número de ficha ya está registrado en el sistema"
                )
        
        ficha_obj.Id_Car = id_carrera_nueva
        ficha_obj.Num_Fic = nuevo_numero_ficha
        ficha_obj.Fec_inicio_Fic = nueva_fecha_inicio
        ficha_obj.Fec_Fin_Fic = nueva_fecha_fin
        ficha_obj.Jor_Fic = nueva_jornada

        db.session.commit()
        return redirect(url_for("token.module_token_config"))
        
    return render_template(
        "C_Alter_Token.html",
        carrera_actual=carrera_obj,
        ficha=ficha_obj,
        career_avaliable=career_avaliable,
        user=coordinador_data
    )


@token_bp.route("/Delete_token/<int:career>/<int:token_value>", methods=["GET", "POST"])
def Delete_token(career, token_value):
    id_actual = session.get('user_id')
    role_actual = session.get('role')
    
    if not id_actual or role_actual != 'Coordinador':
        return redirect(url_for("home"))
    
    coordinador_data = Administrador.query.get(id_actual)
    if not coordinador_data:
        return redirect(url_for("home"))

    ficha_obj = Fichas.query.filter_by(Id_Car=career, Num_Fic=token_value).first()
  
    if not ficha_obj:
        return redirect(url_for("token.module_token_config"))

    if request.method == "POST":
    
        db.session.delete(ficha_obj)
        db.session.commit()
        return redirect(url_for("token.module_token_config"))
    
    return render_template(
        "C_Delete_Token.html",
        career=career,
        token_value=token_value,
        ficha=ficha_obj,
        user=coordinador_data
    )
