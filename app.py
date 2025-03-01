import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from extensions import db, ma, bcrypt, jwt
from services.login_and_registration.router import auth_bp
from services.resume_extraction.router import resume_bp
from utility.common_login import login_manager
from services.admin.router import admin_bp


app = Flask(__name__)

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config.from_object(Config)


login_manager.init_app(app)


db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
