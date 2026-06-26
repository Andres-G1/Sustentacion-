from flask import Blueprint, request, render_template, url_for, redirect, session
from database import career, users

career_bp = Blueprint('career', __name__, url_prefix="/career")

@career_bp.route("/module_career_config")
def module_career_config():
    id_actual = session.get('user_id')
    if id_actual in users:
        return render_template("Career_config.html", career=career, user=users[id_actual])
    return redirect(url_for("home"))

   