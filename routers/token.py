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

