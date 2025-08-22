import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLITE = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', DEFAULT_SQLITE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
