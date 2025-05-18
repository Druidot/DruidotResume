import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///resumedb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = "supersecretkey"
    UPLOAD_FOLDER = 'uploads'
    WEBSITE_NAME = os.getenv("WEBSITE_NAME", "Default App Name")
    LOGO_PATH = os.getenv("LOGO_PATH", "/static/img/logo.jpeg")
    COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "default@example.com")
    SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "+91-0000000000")
    TAG_LINE = os.getenv("TAG_LINE", "This is HR Agency")
    MEDIA_FOLDER = os.path.join(BASE_DIR, 'media')








