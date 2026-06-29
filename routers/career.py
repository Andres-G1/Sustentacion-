from flask import Blueprint, request, render_template, url_for, redirect, session
from database import career, users, token

career_bp = Blueprint('career', __name__, url_prefix="/career")

@career_bp.route("/module_career_config")
def module_career_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Career_config.html", career=career, user=users[id_actual])
    return redirect(url_for("home"))

@career_bp.route("/Create_career", methods=["GET", "POST"])
def Create_career():

    id_actual = session.get('user_id')

    if request.method == 'POST' and id_actual in users:

        new_career = request.form.get('career')

        if new_career not in career["career"]:

            career["career"].append(new_career)
            token[new_career] = []

            return redirect(url_for("coordinador.coordinador"))
        
        else:

            return render_template(
                "C_Create_Career.html",
                error="Carrera existente",
            )
        
    return render_template(
        "C_Create_Career.html",
        user = users[id_actual]
    )

@career_bp.route("/Alter_career/<career_name>", methods=["GET", "POST"])
def Alter_career(career_name):
    
    id_actual = session.get('user_id')
    
    if career_name not in career["career"]:
        return redirect(url_for("coordinador.coordinador"))
    
    if request.method == "POST" and id_actual in users:
        
        new_career_name = request.form.get('career')
        
        if new_career_name and new_career_name != career_name:
            # Verificar que el nuevo nombre no exista
            if new_career_name not in career["career"]:
                # Actualizar en career
                index = career["career"].index(career_name)
                career["career"][index] = new_career_name
                
                # Actualizar en token (renombrar la clave)
                if career_name in token:
                    token[new_career_name] = token.pop(career_name)
                
                return redirect(url_for("coordinador.coordinador"))
            else:
                return render_template(
                    "C_Alter_Career.html",
                    career_name=career_name,
                    error="Carrera existente",
                    user=users[id_actual]
                )
    
    return render_template(
        "C_Alter_Career.html",
        career_name=career_name,
        user=users[id_actual]
    )

@career_bp.route("/Delete_career/<career_name>", methods=["GET", "POST"])
def Delete_career(career_name):
    
    id_actual = session.get('user_id')
    
    if career_name not in career["career"]:
        return redirect(url_for("coordinador.coordinador"))
    
    if request.method == "POST" and id_actual in users:
        
        career["career"].remove(career_name)
        
        if career_name in token:
            token.pop(career_name)
        
        return redirect(url_for("coordinador.coordinador"))
    
    return render_template(
        "C_Delete_Career.html",
        career_name=career_name,
        user=users[id_actual]
    )