from extensions import db
from services.login_and_registration.model import User
from services.login_and_registration.utility import hash_password, check_password


def get_user_by_email(email: str):
    """Fetch user by email from the database."""
    return User.query.filter_by(email=email).first()  # Returns None if not found

def register_user(data):
    new_user = User(username=data.username, email=data.email, password=hash_password(data.password))
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully"}

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password(password, user.password):
        return user
    return None
