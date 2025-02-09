from flask_login import login_user, logout_user, login_required, current_user,LoginManager

from services.login_and_registration.model import User

login_manager = LoginManager()
login_manager.login_view = "auth.login_page"  # Redirect to login page if not authenticated


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 