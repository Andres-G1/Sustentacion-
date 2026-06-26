from flask import Flask, request, render_template
from routers.login import user_bp
from routers.aprendiz import aprendiz_bp
from routers.coordinador import coordinador_bp
from routers.instructor import instructor_bp
from database import users

app = Flask(__name__)

app.secret_key = '2122022025' 

@app.route("/")
def home():
    return render_template("login.html")

app.register_blueprint(user_bp)

app.register_blueprint(aprendiz_bp)

app.register_blueprint(coordinador_bp)

app.register_blueprint(instructor_bp)

if __name__ == "__main__":
    app.run(debug=True)
