import shutil
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
from docx import Document

from datetime import datetime
import os
import re
from pdfminer.high_level import extract_text
import csv
from resume_extractor import ResumeExtractor
from skills_expericence import extract_skills_and_experience, load_skills_from_csv

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def clear_folder(folder_path):
    if os.path.exists(folder_path):  # Ensure the folder exists
        for filename in os.listdir(folder_path):  # List all files in the folder
            file_path = os.path.join(folder_path, filename)  # Full path to the file
            try:
                if os.path.isfile(file_path):  # Check if it's a file
                    os.unlink(file_path)  # Delete the file
                elif os.path.isdir(file_path):  # Check if it's a directory
                    shutil.rmtree(file_path)  # Delete the directory
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The folder {folder_path} does not exist.")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def remove_duplicate(skills_list):
    new_skills_list = []
    for skill in skills_list:
        if skill not in new_skills_list and skill.lower() not in new_skills_list:
            new_skills_list.append(skill)
    return new_skills_list

def parse_experience_input(experience_input):
    """
    Parses the provided experience input and returns a tuple (min_years, max_years).
    Handles formats like:
    - "Fresher" -> (0, 0)
    - "2 years" -> (2, 2)
    - "1 years" -> (1, 1)
    - "0-1 years" -> (0, 1)
    """
    experience_input = experience_input.lower().strip()
    if experience_input == "fresher":
        return 0, 0
    elif "-" in experience_input:
        match = re.match(r"(\d+)-(\d+)\s*years", experience_input)
        if match:
            return int(match.group(1)), int(match.group(2))
    else:
        match = re.match(r"(\d+)\s*years", experience_input)
        if match:
            value = int(match.group(1))
            return value, value
    raise ValueError(f"Invalid experience input format: {experience_input}")


def calculate_total_years(experience):
    """
    Converts experience dict to total years as a float.
    Example: {'years': 1, 'months': 6} -> 1.5
    """
    years = experience.get("years", 0)
    months = experience.get("months", 0)
    total_years = years + (months / 12.0)
    return total_years


def is_experience_in_range(experience, experience_input):
    """
    Checks if the extracted experience falls within the provided experience input range.
    """
    min_years, max_years = parse_experience_input(experience_input)
    total_years = calculate_total_years(experience)
    return min_years <= total_years <= max_years

def matches_criteria(details, skill_set, experience_range):
    """
    Checks if the extracted resume details match the given criteria.
    """
    resume_experience = details.get("Experience_cal", "")
    if resume_experience == 'Fresher':
        resume_experience = {'years':0,'months':0}
    if not is_experience_in_range(resume_experience,experience_range):
        return False

    matched_skills = set(details.get("Matched Skills", []))
    required_skills = skill_set
   
    if len(matched_skills) == 0:
        return False

    return True

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""
    
def extract_text_from_docx(docx_file):
    try:
    # Load the docx file
        doc = Document(docx_file)
        
        # Initialize an empty string to hold the extracted text
        full_text = []
        
        # Loop through each paragraph in the document
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        
        # Join all paragraphs into a single string with line breaks
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading {docx_file}: {e}")
        return ""

def extract_resume_data(job_desc,skill_set,experience_range,experience_range_dict):
    resume_directory = "uploads/"
    output_file = "resume_details.csv"
    resume_data = []

    with open(output_file, mode="w", newline="") as file:
        fieldnames = [
            "Name", "Mobile", "Email", "Skills", "Experience", "Matched Skills",
            "Certifications", "Education", "Summary", "Location", "Score"
        ]
        for file_name in os.listdir(resume_directory):
                try:
                    
                    file_path = os.path.join(resume_directory, file_name)

                    if file_name.endswith(".pdf"):
                        resume_text = extract_text_from_pdf(file_path)
                    elif file_name.endswith(".docx"):
                        resume_text = extract_text_from_docx(file_path)
                        print("resume_text======>",resume_text)
                    else:
                        continue

                    sections = ResumeExtractor.split_into_sections(resume_text) #passed
                    certifications = ResumeExtractor.extract_certifications(sections) #passed
                    education = ResumeExtractor.extract_education(sections) #passed
                    summary = ResumeExtractor.extract_summary(sections) #passed
                    preprocessed_text = ResumeExtractor.preprocess_text(resume_text) #passed
                    details = ResumeExtractor.extract_details(preprocessed_text, skill_set) #passed
                    experience_extracted = ResumeExtractor.extract_experience(sections)
                    if len(experience_extracted) != 0:
                        experience_extracted = experience_extracted[-1]['total_experiences']
                    matched_skills = details['Skills']
                    location = ResumeExtractor.extract_location(resume_text)
                    projects = ResumeExtractor.extract_projects(sections)
                    achievements = ResumeExtractor.extract_achievements(sections)



                    details.update({
                        "Matched Skills": matched_skills,
                        "Experience_cal":{"years":0,"months":0},
                        "Experience":'',
                        "Certifications": certifications,
                        "Education": education,
                        "Summary": summary,
                        "Location": location,
                        "Projects":projects,
                        'Achievements': achievements,
                        'resume' : file_path

                    })

                    if len(experience_extracted) != 0:
                        details["Experience_cal"] = experience_extracted
                        details["Experience"] = f"{experience_extracted['years']} years {experience_extracted['months']} months" if type(experience_extracted) != str else experience_extracted,

                    # Calculate resume score
                    score = ResumeExtractor.calculate_resume_score(details, matched_skills,skill_set,experience_range_dict)
                    details["Score"] = round(score, 2)

                    

                    if matches_criteria(details, set(skill_set), experience_range):
                        resume_data.append(details)
                        print(f"Added {file_name} to the output.")
                    else:
                        print(f"Skipped {file_name}: does not match criteria.")

                except Exception as e:
                    print(f"Error processing {file_name}: {e}")

    print(f"Filtered resume details saved to {output_file}")

    return resume_data


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_resumes', methods=['POST'])
def process_resumes():
    if request.method == 'POST':

        clear_folder(app.config['UPLOAD_FOLDER'])
        job_description = request.form.get('jobDescription')
        

                # Example usage
        current_directory = os.getcwd()
        csv_file_path = 'skills_set.csv'  # Replace with the path to your skills CSV file
        csv_file_path = os.path.join(current_directory, csv_file_path)
        skills = load_skills_from_csv(csv_file_path)
        result = extract_skills_and_experience(job_description, skills)

        print("result==>",result)
        
        
        skills_set = result['skills']
        minexperience = result['experience'][0]
        maxexperience = result['experience'][1]

        if minexperience == maxexperience :
            maxexperience = maxexperience + 10

        experience = f'{minexperience}-{maxexperience} years'
        experience_range_dict = {'min':minexperience,'max':maxexperience}


        # location = request.form.get('location')
        files = request.files.getlist('resumes')

        if not (job_description and skills_set and maxexperience and maxexperience and files):
            return jsonify({"success": False, "message": "All fields are required"})


        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

        resumedata = extract_resume_data(job_description,skills_set,experience,experience_range_dict)

        given_data = {
            "skills_set":skills_set,
            "experience":experience,
            "job_desc":job_description
        }

        return jsonify({"success": True, "resumes": resumedata,'given_data':given_data})


if __name__ == '__main__':
    app.run(debug=True)
