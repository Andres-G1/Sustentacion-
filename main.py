import os
from flask import Flask, request, render_template
from routers.login import user_bp
from routers.aprendiz import aprendiz_bp
from routers.instructor import instructor_bp
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

if __name__ == "__main__":
    app.run(debug=True)

#pip install python-dotenv pymysql flask-sqlalchemy