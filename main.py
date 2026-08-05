import os
from flask import Flask, request, render_template
from routers.login import user_bp
from routers.aprendiz import aprendiz_bp
from routers.instructor import instructor_bp
from routers.coordinador import coordinador_bp
from routers.token import token_bp
from routers.career import career_bp
from database import db, get_database_uri

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("login.html")

app.register_blueprint(user_bp)

app.register_blueprint(aprendiz_bp)

app.register_blueprint(instructor_bp)

app.register_blueprint(coordinador_bp)

app.register_blueprint(token_bp)

app.register_blueprint(career_bp)

if __name__ == "__main__":
    app.run(debug=True)

#pip install python-dotenv pymysql flask-sqlalchemy
#uv run python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('123456'))"
'''uv run python -c "
from werkzeug.security import generate_password_hash
print('Instructor:', generate_password_hash('123456'))
print('Administrador:', generate_password_hash('123456'))
"'''
