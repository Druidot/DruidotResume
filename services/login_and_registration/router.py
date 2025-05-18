from datetime import datetime
import os
from typing import Counter
from flask import Blueprint, app, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_pydantic import validate
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from services.admin.model import Organization
from services.login_and_registration.model import Profile, User
from services.login_and_registration.schema import UserRegisterSchema, UserLoginSchema
from services.login_and_registration.service import get_user_by_email, register_user, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
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

@auth_bp.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('media', filename)

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
    if not user:
        flash("Invalid credentials", "danger")
    if not user.is_verified:
        flash("Your Account is not verified by admin", "danger")  
    elif user and user.is_active:
        login_user(user)
        return redirect(url_for('auth.dashboard'))  
    else:
        flash("Invalid credentials", "danger")  
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

    organization = Organization.query.first()
    if not organization:
        return redirect(url_for("auth.register_organization"))

    if current_user.is_admin:
        users = User.query.all()

        total_users = len(users)

        if total_users == 0:
            return jsonify({
                "total_users": 0,
                "admin_percentage": 0.0,
                "user_percentage": 0.0,
                "customer_percentage": 0.0
            })

        # Count roles
        role_counts = Counter(user.roles for user in users)

        # Get counts (default to 0 if role not found)
        admin_count = role_counts.get("admin", 0)
        user_count = role_counts.get("user", 0)
        customer_count = role_counts.get("customer", 0)

        active_users = sum(user.is_active for user in users)
        verified_users = sum(user.is_verified for user in users)

        # Calculate percentages
        admin_percentage = round((admin_count / total_users) * 100, 2)
        user_percentage = round((user_count / total_users) * 100, 2)
        customer_percentage = round((customer_count / total_users) * 100, 2)
        # return render_template('./frontend/admin_pannel.html', users=users)
        return render_template('./admin_pannels/dashboard.html', users=users,
                               admin_percentage=admin_percentage, 
                               user_percentage=user_percentage, 
                               customer_percentage=customer_percentage,
                               active_users=active_users,
                               verified_users=verified_users,
                               total_users=total_users)

    return render_template('./screens/homepage.html')




@auth_bp.route('/customers', methods=['GET'])
def get_active_verified_customers():
    # Efficiently query the database with filters
    customers = User.query.filter_by(roles='customer', is_active=True, is_verified=True).all()

    # Convert SQLAlchemy objects to dictionaries for JSON response
    customer_data = [
        {
            "id": customer.id,
            "username": customer.username,
            "email": customer.email,
            "roles": customer.roles
        } for customer in customers
    ]

    return jsonify(customer_data), 200


@auth_bp.route("/profile/save", methods=["POST"])
@login_required
def save_profile():
    user_id = current_user.id  # Get from session or form

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for("auth.dashboard"))


    # Get or create profile
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)

    profile.full_name = request.form.get("full_name")
    profile.mobile = request.form.get("mobile")
    dob_str = request.form.get("dob")
    if dob_str:
        profile.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    profile.city = request.form.get("city")
    profile.state = request.form.get("state")
    profile.country = request.form.get("country")
    profile.address = request.form.get("address")
    profile.role = request.form.get("role")
    profile.gender = request.form.get("gender")
    profile.about = request.form.get("about")

    # Profile picture upload
    pic = request.files.get("profile_picture")
    if pic and pic.filename:
        filename = secure_filename(pic.filename)
        
        folder = os.path.join('media', 'profile_pic')
        os.makedirs(folder, exist_ok=True) 

        filepath = os.path.join(folder, filename)  
        pic.save(filepath)

        # Save just the relative filename if needed for DB
        profile.profile_picture = os.path.join('profile_pic', filename)

    db.session.add(profile)
    db.session.commit()
    flash("Profile updated successfully!")
    return redirect(url_for("auth.dashboard"))




@auth_bp.route('/organization/register', methods=['GET','POST'])
@login_required
def register_organization():
    user_id = current_user.id
    if request.method == 'POST':
        title = request.form['title']
        logo_file = request.files['logo']

        if logo_file:
            filename = secure_filename(logo_file.filename)
            filepath = os.path.join('.\media\logo', filename)
            logo_file.save(filepath)
            organization = Organization.query.filter_by(user_id=user_id).first()
            if not organization:
                organization = Organization(user_id=user_id)

            
            organization.title=title
            organization.logo_path=filepath
            organization.created_by="owner"  # auto manage this or take from session
            organization.updated_by="owner"
            organization.created_dt=datetime.now()
            organization.updated_dt=datetime.now()

            db.session.add(organization)
            db.session.commit()
            return redirect(url_for("auth.dashboard"))
    else:
        return render_template('./admin_pannels/organization_register.html')




