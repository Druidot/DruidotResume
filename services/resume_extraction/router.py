import os
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_pydantic import validate
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from services.login_and_registration.model import User
from services.login_and_registration.schema import UserRegisterSchema, UserLoginSchema
from services.login_and_registration.service import get_user_by_email, register_user, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user

from utility.error_messages import error_messages
from utility.resume_services.resume_extractor import ResumeExtractor
from utility.resume_services.skills_expericence import extract_skills_and_experience, load_skills_from_csv
from utility.resume_services.common_functions import clear_folder, extract_resume_data, remove_duplicate, parse_experience_input, calculate_total_years
from config import Config
resume_bp = Blueprint("resume", __name__, url_prefix="/resume")




@resume_bp.route("/resume_extraction", methods=["GET"])
@login_required
def resume_extraction():
    return render_template('./resume/resume.html')



@resume_bp.route('/process_resumes', methods=['POST'])
def process_resumes():
    if request.method == 'POST':
        clear_folder(Config.UPLOAD_FOLDER)
        job_description = request.form.get('jobDescription')
        
        current_directory = os.getcwd()
        csv_file_path = 'skills_set.csv'  # Replace with the path to your skills CSV file
        csv_file_path = os.path.join(current_directory, csv_file_path)
        skills = load_skills_from_csv(csv_file_path)
        result = extract_skills_and_experience(job_description, skills)

        
        
        skills_set = result['skills']
        minexperience = result['experience'][0]
        maxexperience = result['experience'][1]

        if minexperience == maxexperience :
            maxexperience = maxexperience + 10

        experience = f'{minexperience}-{maxexperience} years'
        experience_range_dict = {'min':minexperience,'max':maxexperience}


        files = request.files.getlist('resumes')

        if not (job_description and skills_set and maxexperience and maxexperience and files):
            return jsonify({"success": False, "message": "All fields are required"})


        for file in files:
            file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
            file.save(file_path)

        resumedata = extract_resume_data(job_description,skills_set,experience,experience_range_dict)

        given_data = {
            "skills_set":skills_set,
            "experience":experience,
            "job_desc":job_description
        }

        return jsonify({"success": True, "resumes": resumedata,'given_data':given_data})

