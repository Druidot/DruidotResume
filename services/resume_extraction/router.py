import os
from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_pydantic import validate
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from services.admin.model import ManagerJobdescriptionModel
from services.login_and_registration.model import User
from services.login_and_registration.schema import UserRegisterSchema, UserLoginSchema
from services.login_and_registration.service import get_user_by_email, register_user, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user

from services.resume_extraction.model import CandidateModel
from utility.error_messages import error_messages
from utility.resume_services.resume_extractor import ResumeExtractor
from utility.resume_services.skills_expericence import extract_skills_and_experience, load_skills_from_csv
from utility.resume_services.common_functions import clear_folder, extract_resume_data, remove_duplicate, parse_experience_input, calculate_total_years
from config import Config
from extensions import db

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")




@resume_bp.route("/resume_extraction/<int:job_id>", methods=["GET"])
@login_required
def resume_extraction(job_id):
    job_data = ManagerJobdescriptionModel.query.filter_by(id=job_id).first()
    return render_template('./resume/resume.html',job_data=job_data)

@resume_bp.route("/resume_grid/<int:job_id>", methods=["GET"])
@login_required
def resume_grid(job_id):
    job_data = CandidateModel.query.filter_by(job_description_id=job_id).all()
    return render_template('./resume/canditate_grid.html',job_data=job_data)

@resume_bp.route("/candidate_information/<int:id>", methods=["GET"])
@login_required
def candidate_information(id):
    candidate_information_data = CandidateModel.query.filter_by(id=id).first()
    return render_template('./resume/candidate_information.html', candidate_information_data=candidate_information_data)



@resume_bp.route('/candidate_resume/<int:candidate_id>', methods=['GET'])
@login_required
def serve_resume(candidate_id):
    candidate_information_data = CandidateModel.query.filter_by(id=candidate_id).first()
    if not candidate_information_data:
        abort(404, description="Candidate not found")
    
    resume_filename = candidate_information_data.resume_file
    file_path = os.path.join(resume_filename)

    if os.path.isfile(file_path):
        file_name = resume_filename.split('/')[-1]
        return send_from_directory(Config.UPLOAD_FOLDER,file_name, as_attachment=True)
    else:
        abort(404, description=f"Resume file not found {file_path}")

@resume_bp.route('/select_candidate', methods=['POST'])
def select_candidate():
    data = request.get_json()
    candidate_id = data.get('candidate_id')
    job_description_id = data.get('job_description_id')

    try:
        candidate = CandidateModel.query.filter_by(id=candidate_id, job_description_id=job_description_id).first()

        if not candidate:
            return jsonify({"error": "Candidate not found"}), 404
        if  candidate.candidate_selected:
            candidate.candidate_selected = False
            status = "unselected"
        else:
            candidate.candidate_selected = True
            status = "selected"
        db.session.commit()

        return jsonify({"message": f"Candidate {status} successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


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



@resume_bp.route('/add/candidates', methods=['POST'])
def add_candidates():
    data = request.get_json().get('candidates')
    job_description_id = request.get_json().get('job_id')
    try:
        for data in data:
            existing_candidate = CandidateModel.query.filter_by(
                name=data.get('Name'),
                phone_number=data.get('Mobile', [''])[0] if data.get('Mobile') else '',
                email=data.get('Email'),
                job_description_id = job_description_id
            ).first()
            if existing_candidate:
                # If the candidate already exists, skip adding them
                continue
            new_candidate = CandidateModel(
                name=data.get('Name'),
                phone_number=data.get('Mobile', [''])[0] if data.get('Mobile') else '',
                email=data.get('Email'),
                experience_years=data.get('Experience_cal', {}).get('years', 0),
                experience_months=data.get('Experience_cal', {}).get('months', 0),
                skills=','.join(data.get('Skills', [])),
                score=data.get('Score'),
                resume_file=data.get('resume'),
                location=data.get('Location'),
                certifications=data.get('Certifications'),

                education_degree=data.get('Education', [{}])[1].get('degree') if len(data.get('Education', [])) > 1 else None,
                education_university=data.get('Education', [{}])[1].get('university') if len(data.get('Education', [])) > 1 else None,
                education_duration=data.get('Education', [{}])[1].get('duration') if len(data.get('Education', [])) > 1 else None,
                education_grade=data.get('Education', [{}])[1].get('grade') if len(data.get('Education', [])) > 1 else None,

                project_title=data.get('Projects', [{}])[0].get('title') if data.get('Projects') else None,
                project_description=data.get('Projects', [{}])[0].get('description') if data.get('Projects') else None,
                job_description_id = job_description_id
            )

            db.session.add(new_candidate)
            job_data = ManagerJobdescriptionModel.query.filter_by(id=job_description_id).first()
            if job_data:
                job_data.resume_process_count += 1
                job_data.updated_dt = db.func.now()
                job_data.updated_by = current_user.username
            db.session.commit()

        return jsonify({"message": "Candidate added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@resume_bp.route('/view/candidates/<int:id>', methods=['GET'])
def get_candidate(id):
    candidate = CandidateModel.query.get(id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    candidate_data = {
        "Name": candidate.name,
        "Mobile": [candidate.phone_number],
        "Email": candidate.email,
        "Experience": f"{candidate.experience_years} years {candidate.experience_months} months",
        "Skills": candidate.skills.split(','),
        "Score": candidate.score,
        "Location": candidate.location,
        "Certifications": candidate.certifications,
        "Education": {
            "degree": candidate.education_degree,
            "university": candidate.education_university,
            "duration": candidate.education_duration,
            "grade": candidate.education_grade
        },
        "Projects": {
            "title": candidate.project_title,
            "description": candidate.project_description
        }
    }

    return jsonify(candidate_data), 200