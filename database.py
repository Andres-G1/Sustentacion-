import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv("credencial.env")

db = SQLAlchemy()

def get_database_uri():
    return (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

'''
uv add flask-sqlalchemy pymysql
uv add python.dotenv
212202
'''