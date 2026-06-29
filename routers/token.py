from flask import Blueprint, request, render_template, url_for, redirect, session
from database import token, career, attendance, users 

token_bp = Blueprint('token', __name__, url_prefix="/token")

@token_bp.route ("/module_token_config")
def module_token_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Token_config.html", token=token, user=users[id_actual])
    return redirect(url_for("home"))

@token_bp.route("/Create_token", methods=["GET", "POST"])
def Create_token():

    career_avaliable = career.get("career")

    id_actual = session.get('user_id')

    if request.method == 'POST' and id_actual in users:

        Career = request.form.get('career')
        new_token = request.form.get("token")

        if new_token not in token[Career]:  

            token[Career].append(new_token)  # 

            return redirect(url_for("coordinador.coordinador"))
        
    return render_template(
        "C_Create_Token.html",
        career_avaliable=career_avaliable,
        user = users[id_actual]
    )

@token_bp.route("/Alter_token/<career>/<old_token>", methods=["GET", "POST"])
def Alter_token(career, old_token):
    
    id_actual = session.get('user_id')
    
    if career not in token or old_token not in token[career]:
        return redirect(url_for("coordinador.coordinador"))
    
    if request.method == "POST" and id_actual in users:
        
        new_token_value = request.form.get('token')
        
        if new_token_value and new_token_value != old_token:

            if new_token_value not in token[career]:

                index = token[career].index(old_token)
                token[career][index] = new_token_value
                
                return redirect(url_for("token.module_token_config"))
            else:
                return render_template(
                    "C_Alter_Token.html",
                    career=career,
                    old_token=old_token,
                    error="Token ya existe en esta carrera",
                    user=users[id_actual]
                )
    
    return render_template(
        "C_Alter_Token.html",
        career=career,
        old_token=old_token,
        user=users[id_actual]
    )

@token_bp.route("/Delete_token/<career>/<token_value>", methods=["GET", "POST"])
def Delete_token(career, token_value):
    
    id_actual = session.get('user_id')
    
    if career not in token or token_value not in token[career]:
        return redirect(url_for("coordinador.coordinador"))
    
    if request.method == "POST" and id_actual in users:
        
        token[career].remove(token_value)
        
        return redirect(url_for("token.module_token_config"))
    
    return render_template(
        "C_Delete_Token.html",
        career=career,
        token_value=token_value,
        user=users[id_actual]
    )

