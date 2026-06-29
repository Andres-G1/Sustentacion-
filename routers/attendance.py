from flask import Blueprint, request, render_template, url_for, redirect, session
from database import token, career, attendance

attendance_bp = Blueprint('attendance', __name__, url_prefix="/attendance")

@attendance_bp.route("/create_attendance", methods=["GET", "POST"])
def create_attendace_token():
    return render_template()