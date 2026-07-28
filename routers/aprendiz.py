from flask import Blueprint, request, render_template, url_for, redirect, session
from models.models import Aprendiz

aprendiz_bp = Blueprint('aprendiz', __name__, url_prefix="/aprendiz")

@aprendiz_bp.route("/aprendiz")
def aprendiz():
    id_actual = session.get('user_id')
    role_actual = session.get('role')

    if id_actual and role_actual == 'Aprendiz':
        aprendiz_data = Aprendiz.query.get(id_actual)
        if aprendiz_data:
            return render_template("module_A.html", user=aprendiz_data)

    return redirect(url_for("home"))