from flask import Blueprint, request, render_template, url_for, redirect, session
from database import token, career, attendance

attendance_bp = Blueprint('attendance', __name__, url_prefix="/attendance")

@attendance_bp.route("/create_token", methods=["GET", "POST"])
def create_token():
    if request.method == "POST":
        career = request.form.get("career")
        num_token= request.form.get("num_token")

        if career not in token:
            return redirect(url_for("coordinador.coordinador_create_A"))
        else:
            return render_template(
                "C_Create_Aprendiz.html",
            )

    return render_template(
        "C_Create_Aprendiz.html",
    )