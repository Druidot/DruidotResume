import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///resumedb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = "supersecretkey"
    UPLOAD_FOLDER = 'uploads'

