from flask import Blueprint, request, render_template, url_for, redirect, session
from database import token, career, attendance
token_bp = Blueprint('token', __name__, url_prefix="/token")
