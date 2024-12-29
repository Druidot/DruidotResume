import csv
import re

def load_skills_from_csv(csv_file_path):
    """
    Loads skills from a CSV file and returns them as a list.
    Args:
        csv_file_path (str): Path to the CSV file.
    Returns:
        list: A list of skills extracted from the CSV.
    """
    skills = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            skills.append(row[0].strip())  # Assuming skills are in the first column
    return skills

def extract_skills_and_experience(job_description, skills):
    """
    Extracts skills and experience from a job description using predefined skills.

    Args:
        job_description (str): The job description text.
        skills (list): List of predefined skills to search for.
    
    Returns:
        dict: A dictionary with 'skills' and 'experience' extracted from the job description.
    """
    # Improved regex pattern for experience
    # experience_pattern = r"(\d+)\s*(?:to|[-–])\s*(\d+)\s*(?:years|yr)|(?:minimum|at\s*least|over)\s*(\d+)\s*(?:years|yr)|(\d+)\s*(?:years|yr)"
    # experience_pattern = r"(\d+)\s*(?:to|[-–])\s*(\d+)\s*(?:years|yr)|(?:minimum|at\s*least|over)\s*(\d+)\s*(?:years|yr)|(\d+)\s*(?:years|yr)|(\d+)\s*\+?\s*(?:years|yr)"


    experience_pattern = r"(\d+)\s*(?:to|[-–])\s*(\d+)\s*(?:years|yr)|(?:minimum|at\s*least|over)\s*(\d+)\s*(?:years|yr)|(\d+)\s*(?:years|yr)|(\d+)\s*\+?\s*(?:years|yr)|(\d+)\s*\+\s*(?:years|yrs)"


    # Extract experience using regex
    experience_matches = re.findall(experience_pattern, job_description, re.IGNORECASE)

    print(experience_matches)

    min_experience, max_experience = None, None

    # for match in experience_matches:
    #     if match[0] and match[1]:  # Matches like '2–5 years' or '2-5 years'
    #         min_experience = int(match[0])
    #         max_experience = int(match[1])
    #     elif match[2]:  # Matches like 'minimum 3 years'
    #         min_experience = int(match[2])
    #     elif match[3]:  # Matches like '3 years'
    #         min_experience = int(match[3])
    #         max_experience = min_experience  # If there's no range, set max as min

    for match in experience_matches:
    # Create a list of all matched groups that are non-empty
        non_empty_groups = [int(group) for group in match if group]

        if len(non_empty_groups) == 2:  # Range like '2-5 years'
            min_experience, max_experience = non_empty_groups
        elif len(non_empty_groups) == 1:  # Single value like '2 years' or '2+ years'
            min_experience = non_empty_groups[0]
            max_experience = None if '+' in match else min_experience  # Handle "2+ years"

    # Check if experience values are still None and update if necessary
    if min_experience is None:
        min_experience = 0
    if max_experience is None:
        max_experience = min_experience

    # Convert the job description into lowercase for case-insensitive matching
    job_description_lower = job_description.lower()

    # Extract skills from the job description by checking against predefined skills
    extracted_skills = [skill for skill in skills if skill.lower() in job_description_lower]

    # Return the skills as a comma-separated string
    extracted_skills = list(sorted(set(extracted_skills), key=lambda x: x.lower()))

    # Return the extracted data
    return {
        'skills': extracted_skills,
        'experience': (min_experience, max_experience)
    }



