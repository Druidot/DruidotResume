from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_pydantic import validate
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from services.login_and_registration.model import User
from services.login_and_registration.schema import UserRegisterSchema, UserLoginSchema
from services.login_and_registration.service import get_user_by_email, register_user, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user

from utility.error_messages import error_messages



auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


#-----------------------------------------------APIs Rendering-----------------------------------------------#


@auth_bp.route("/api/register", methods=["POST"])
@validate()
def api_register(body: UserRegisterSchema):
    return jsonify(register_user(body))

@auth_bp.route("/api/login", methods=["POST"])
@validate()
def api_login(body: UserLoginSchema):
    user = authenticate_user(body.email, body.password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token})
    return jsonify({"error": "Invalid credentials"}), 401





#-----------------------------------------------Template Rendering-----------------------------------------------#

@auth_bp.route("/login_page", methods=["GET"])
def login_page():
    return render_template('./frontend/login_registration.html')


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.form.to_dict()

    try:
        user_data = UserRegisterSchema(**data)
    except ValidationError as e:
        error_messages(e)
        return redirect(url_for("auth.login_page")) 

    existing_user = get_user_by_email(user_data.email)  
    if existing_user:
        flash("Email is already registered. Try logging in.", "error")
        return redirect(url_for("auth.login_page"))

    register_user(user_data) 
    flash("Registration successful! You can now log in.", "success")
    
    return redirect(url_for("auth.login_page")) 


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form.to_dict()

    try:
        user_data = UserLoginSchema(**data)
    except ValidationError as e:
        error_messages(e)
        return redirect(url_for("auth.login_page"))

    user = authenticate_user(user_data.email, user_data.password)
    if user:
        login_user(user)
        return redirect(url_for('auth.dashboard'))  
    flash("Invalid credentials", "error")  
    return redirect(url_for("auth.login_page")) 



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login_page"))



@auth_bp.route("/dashboard", methods=["GET"])
@validate()
@login_required
def dashboard():
    return render_template('./frontend/dashboard_main.html')


