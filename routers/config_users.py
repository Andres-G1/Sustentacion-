from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users

config_bp = Blueprint('config', __name__, url_prefix="/config")

@config_bp.route("/module_config", methods=["GET", "POST"])
def module_config():
    id_actual = session.get('user_id') 
    

    if id_actual in users: 
        return render_template("module_Config.html", users=users[id_actual]) 
    return redirect(url_for("home"))

@config_bp.route("/porfile_users")
def porfile_users():
    id_actual = session.get('user_id') 
    if id_actual in users: 
        return render_template("porfile_user.html", users=users[id_actual]) 
    return redirect(url_for("home"))   

