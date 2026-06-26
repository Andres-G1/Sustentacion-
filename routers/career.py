from flask import Blueprint, request, render_template, url_for, redirect, session
from database import career, users

career_bp = Blueprint('career', __name__, url_prefix="/career")

@career_bp.route("/module_career_config")
def module_career_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Career_config.html", career=career, user=users[id_actual])
    return redirect(url_for("home"))

@career_bp.route("/Create_token", methods=["GET", "POST"])
def Create_token():

    career_avaliable = career.get("career")

    id_actual = session.get('user_id')

    if request.method == 'POST' and id_actual in users:

        new_career = request.form.get('career')

        if new_career in career:


            return redirect(url_for("coordinador.coordinador"))
        
    return render_template(
        "C_Create_Career.html",
        career_avaliable=career_avaliable,
        user = users[id_actual]
    )