from flask import Blueprint, request, render_template, url_for, redirect, session
from database import users

config_bp = Blueprint('config', __name__, url_prefix="/config")

@config_bp.route("/module_config_aprendiz", methods=["GET", "POST"])
def module_config_aprendiz():
    id_actual = session.get('user_id')

    if id_actual not in users:
        return redirect(url_for("home"))

    mensaje = None
    tipo_mensaje = None 

    if request.method == "POST":
        password_actual = request.form.get('password_actual', '').strip()
        nuevo_email = request.form.get('email', '').strip()
        nueva_password = request.form.get('password', '').strip()

        if password_actual != users[id_actual]['password']:
            mensaje = "La contraseña actual no coincide."
            tipo_mensaje = "error"
        else:
            if nuevo_email:
                users[id_actual]['email'] = nuevo_email

            if nueva_password:
                users[id_actual]['password'] = nueva_password

            mensaje = "Datos actualizados correctamente."
            tipo_mensaje = "success"

            match users[id_actual]["role"]:
                case "Instructor":
                    return redirect(url_for("coordinador.coordinador"))
                case "Aprendiz":
                    return redirect(url_for("aprendiz.aprendiz"))

    return render_template(
        "config_aprendiz.html",
        users=users[id_actual],
        mensaje=mensaje,
        tipo_mensaje=tipo_mensaje
    )

@config_bp.route("/module_config", methods=["GET", "POST"])
def module_config():
    id_actual = session.get('user_id')

    if id_actual not in users:
        return redirect(url_for("home"))

    mensaje = None
    tipo_mensaje = None 

    if request.method == "POST":
        password_actual = request.form.get('password_actual', '').strip()
        nuevo_email = request.form.get('email', '').strip()
        nueva_password = request.form.get('password', '').strip()

        if password_actual != users[id_actual]['password']:
            mensaje = "La contraseña actual no coincide."
            tipo_mensaje = "error"
        else:
            if nuevo_email:
                users[id_actual]['email'] = nuevo_email

            if nueva_password:
                users[id_actual]['password'] = nueva_password

            mensaje = "Datos actualizados correctamente."
            tipo_mensaje = "success"
            return redirect(url_for("coordinador.coordinador"))

    return render_template(
        "config.html",
        user=users[id_actual],
        mensaje=mensaje,
        tipo_mensaje=tipo_mensaje
    )


@config_bp.route("/porfile_users")
def porfile_users():
    id_actual = session.get('user_id') 
    if id_actual in users: 
        return render_template("porfile_user.html", user=users[id_actual]) 
    return redirect(url_for("home"))

@config_bp.route("/porfile_aprendiz")
def porfile_aprendiz():
    id_actual = session.get('user_id') 
    if id_actual in users: 
        return render_template("porfile_aprendiz.html", users=users[id_actual]) 
    return redirect(url_for("home"))      
