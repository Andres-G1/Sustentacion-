from flask import Blueprint, request, render_template, url_for, redirect, session
from werkzeug.security import check_password_hash
from models.models import Aprendiz, Instructor, Administrador

user_bp = Blueprint('users', __name__, url_prefix="/users")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        typeid = request.form.get('typeid')
        num_ide = request.form.get('id')
        password = request.form.get('password')

        aprendiz = Aprendiz.query.filter_by(Tip_ide_Apr=typeid, Num_ide_Apr=num_ide).first()
        instructor = Instructor.query.filter_by(Tip_ide_Ins=typeid, Num_ide_Ins=num_ide).first()
        administrador = Administrador.query.filter_by(Tip_ide_Adm=typeid, Num_ide_Adm=num_ide).first()

        if aprendiz and check_password_hash(aprendiz.Con_Apr, password):
            session['user_id'] = aprendiz.Id_Apr
            session['role'] = 'Aprendiz'
            return redirect(url_for("aprendiz.aprendiz"))

        if instructor and check_password_hash(instructor.Con_Ins, password):
            session['user_id'] = instructor.Id_Ins
            session['role'] = 'Instructor'
            return redirect(url_for("instructor.instructor"))

        if administrador and check_password_hash(administrador.Con_Adm, password):
            session['user_id'] = administrador.Id_Adm
            session['role'] = 'Coordinador'
            return redirect(url_for("coordinador.coordinador"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@user_bp.route("/password")
def password():
    return render_template("Password.html") 