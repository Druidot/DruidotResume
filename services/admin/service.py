
from datetime import datetime
import uuid

from flask_login import current_user
from services.admin.model import Branch, City, Company, Country, Department, Manager, ManagerJobdescriptionModel, ManagerProjectMapModel, Project
from services.login_and_registration.model import User
from extensions import db
from common_functions.response import common_response_api, EnumStatus, EnumResponse

#-------START----------------------------------------make_admin_service------------------------------------------------START--#
def make_admin_service(data):
    user_data = User.query.get(data["user_id"])  
    if not user_data:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message=EnumResponse.USER_NOT_FOUND,
            data=[],
            errors=[EnumResponse.USER_NOT_FOUND],
        )

    if user_data.is_admin:
        user_data.is_admin = False
        db.session.commit()  # Commit the change
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="User is no longer an admin",
            data=[],
            errors=[],
        )

       
    user_data.is_admin = True
    db.session.commit()  # Commit the change
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="User is now an admin",
        data=[],
        errors=[None],
    )
#-------END----------------------------------------make_admin_service------------------------------------------------END--#

#-------START----------------------------------------make_activate_service------------------------------------------------START--#


def make_activate_service(data):
    user_data = User.query.get(data["user_id"])
    if not user_data:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message=EnumResponse.USER_NOT_FOUND,
            data=[],
            errors=[EnumResponse.USER_NOT_FOUND],
        )

    if user_data.is_active:
        user_data.is_active = False
        db.session.commit()  # Commit the change
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="User is no longer active",
            data=[],
            errors=[],
        )

    user_data.is_active = True
    db.session.commit()  # Commit the change
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="User is now active",
        data=[],
        errors=[],
    )

#-------END----------------------------------------make_activate_service------------------------------------------------END--#


#-------START----------------------------------------make_verified_service------------------------------------------------START--#
def make_verified_service(data):
    user_data = User.query.get(data["user_id"])
    if not user_data:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message=EnumResponse.USER_NOT_FOUND,
            data=[],
            errors=[EnumResponse.USER_NOT_FOUND],
        )

    if user_data.is_verified:
        user_data.is_verified = False
        db.session.commit()  # Commit the change
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="User is no longer verified",
            data=[],
            errors=[],
        )

    user_data.is_verified = True
    db.session.commit()  # Commit the change
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="User is now verified",
        data=[],
        errors=[],
    )
#-------END----------------------------------------make_verified_service------------------------------------------------END--#

#-------START----------------------------------------change_role_service------------------------------------------------START--#
def change_role_service(data):
    user_data = User.query.get(data["user_id"])
    if not user_data:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message=EnumResponse.USER_NOT_FOUND,
            data=[],
            errors=[EnumResponse.USER_NOT_FOUND],
        )

    if user_data.roles == data["user_role"]:
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="User role is already set to this value",
            data=[],
            errors=[],
        )

    user_data.roles = data["user_role"]
    db.session.commit()  # Commit the change
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="User role changed successfully",
        data=[],
        errors=[],
    )
#-------END----------------------------------------change_role_service------------------------------------------------END--#

#-------START----------------------------------------get_records_service------------------------------------------------START--#

def get_records_service(table):
    model_map = {
        'company': Company,
        'country': Country,
        'city': City,
        'branch': Branch,
        'department': Department,
        'project': Project,
        'manager': Manager,
        'ManagerProjectMap': ManagerProjectMapModel
    }

    model = model_map.get(table)
    if not model:
        common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="Invalid table name",
            data=[],
            errors=["Invalid table name"],
        )

    records = model.query.all()
    result = []

    for row in records:
        row_data = {col.name: getattr(row, col.name) for col in row.__table__.columns}

        # Add foreign key names
        if isinstance(row, Branch):
            row_data["company_name"] = row.company.company_name if row.company else None
            row_data["city_name"] = row.city.city_name if row.city else None

        if isinstance(row, City):
            row_data["country_name"] = row.country.country_name if row.country else None

        if isinstance(row, Department):
            row_data["branch_name"] = row.branch.branch_name if row.branch else None

        if isinstance(row, Project):
            row_data["department_name"] = row.department.department_name if row.department else None

        if isinstance(row, Manager):
            row_data["manager_name"] = row.user.username if row.user_id else None

        if isinstance(row, ManagerProjectMapModel):
            row_data["manager_name"] = row.manager.user.username if row.manager else None
            row_data["project_name"] = row.project.project_name if row.project else None
            row_data["company_name"] = row.company.company_name if row.company else None
            row_data["city_name"] = row.city.city_name if row.city else None
            row_data["branch_name"] = row.branch.branch_name if row.branch else None
            row_data["department_name"] = row.department.department_name if row.department else None
            


        result.append(row_data)

    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="Records fetched successfully",
        data=result,
        errors=[],
    )   




#-------END----------------------------------------get_records_service------------------------------------------------END--#

#-------START----------------------------------------get_city_by_company_service------------------------------------------------START--#
def get_city_by_company_service(company_id):
    cities = Branch.query.filter_by(company_id=company_id).all()
    managers = Manager.query.filter_by(company_id=company_id).all()
    if not cities and not managers:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="No cities found for this company",
            data=[],
            errors=["No cities found for this company"],
        )
    
    city_list = [{"city_id": city.city_id, "city_name": city.city.city_name} for city in cities]
    manager_list = [{"manager_id": manager.manager_id, "manager_name": manager.user.username} for manager in managers]

    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="Cities and managers fetched successfully",
        data={"city_list": city_list, "manager_list": manager_list},
        errors=[],
    )
#-------END----------------------------------------get_city_by_company_service------------------------------------------------END--#

#-------START----------------------------------------get_city_by_company_service------------------------------------------------START--#
def get_branch_by_city_service(city_id,company_id):
    branches = Branch.query.filter_by(city_id=city_id, company_id=company_id).all()
    branch_list = [{"branch_id": branch.branch_id, "branch_name": branch.branch_name} for branch in branches]
    if not branch_list:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="No branches found for this city",
            data=[],
            errors=["No branches found for this city"],
        )
    else:
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="Branches fetched successfully",
            data=branch_list,
            errors=[],
        )
   

#-------END----------------------------------------get_branch_by_city_service------------------------------------------------END--#

#-------START----------------------------------------get_department_by_branch_service------------------------------------------------START--#
def get_department_by_branch_service(branch_id):
    departments = Department.query.filter_by(branch_id=branch_id).all()
    department_list = [{"department_id": department.department_id, "department_name": department.department_name} for department in departments]
    if not department_list:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="No departments found for this branch",
            data=[],
            errors=["No departments found for this branch"],
        )
    else:
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="Departments fetched successfully",
            data=department_list,
            errors=[],
        )

#-------END----------------------------------------get_department_by_branch_service------------------------------------------------END--#

#-------START----------------------------------------get_project_by_department_service------------------------------------------------START--#
def get_project_by_department_service(department_id):
    
    projects = Project.query.filter_by(department_id=department_id).all()
    project_list = [{"project_id": project.project_id, "project_name": project.project_name} for project in projects]
    if not project_list:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="No projects found for this department",
            data=[],
            errors=["No projects found for this department"],
        )
    else:
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="Projects fetched successfully",
            data=project_list,
            errors=[],
        )
#-------END----------------------------------------get_project_by_department_service------------------------------------------------END--#
#-------START----------------------------------------get_manager_by_project_service------------------------------------------------START--#
def get_manager_by_project_service(project_id):
    managers = ManagerProjectMapModel.query.filter_by(project_id=project_id).all()
    manager_list = [{"manager_id": manager.manager.manager_id, "manager_name": manager.manager.user.username} for manager in managers]
    if not manager_list:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="No managers found for this project",
            data=[],
            errors=["No managers found for this project"],
        )
    else:
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="Managers fetched successfully",
            data=manager_list,
            errors=[],
        )
#-------END----------------------------------------get_manager_by_project_service------------------------------------------------END--#
#-------START----------------------------------------get_manager_project_job_map_service------------------------------------------------START--#
def get_manager_project_job_map_service(project_id):

    job_descriptions = ManagerJobdescriptionModel.query.filter_by(project_id=project_id).all()
    job_description_list = [
        {
            "job_description_id": job.id,
            "job_description": job.job_description,
            "job_title": job.job_title,
            "created_by": job.created_by,
            "updated_by": job.updated_by,
            "remarks": job.remarks,
            "is_active": job.is_active,
            "job_code": job.job_code,
            "job_start_date": job.job_start_date.strftime('%Y-%m-%d') if job.job_start_date else None,
            "job_end_date": job.job_end_date.strftime('%Y-%m-%d') if job.job_end_date else None,
            "job_location": job.job_location,
            "job_type": job.job_type,
            "manager_id": job.manager_id,
            "project_id": job.project_id,
            "resume_process_count": job.resume_process_count,
        }
        for job in job_descriptions
    ]
    if not job_description_list:
        return common_response_api(
            status_code=EnumStatus.NOT_FOUND,
            message="No job descriptions found for this project",
            data=[],
            errors=["No job descriptions found for this project"],
        )
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="Job descriptions fetched successfully",
        data=job_description_list,
        errors=[],
    )

#-------END----------------------------------------get_manager_project_job_map_service------------------------------------------------END--#


#-------START----------------------------------------create_job_description_service------------------------------------------------START--#
def generate_job_code():
    return f"JOB-{uuid.uuid4().hex[:8].upper()}"
def create_job_description_service(data):
    job_code = generate_job_code()
    try:
        job = ManagerJobdescriptionModel(
            manager_id=data['manager_id'],
            project_id=data['project_id'],
            job_description=data['job_description'],
            job_title=data['job_title'],
            created_by=current_user.username,
            updated_by=current_user.username,
            remarks=data.get('remarks'),
            is_active=data.get('is_active', True),
            job_type=data.get('job_type'),
            job_location=data.get('job_location'),
            job_code=job_code,
            job_start_date = datetime.strptime(data.get('job_start_date'), '%Y-%m-%d').date(),
            job_end_date = datetime.strptime(data.get('job_end_date'), '%Y-%m-%d').date()
        )

        db.session.add(job)
        db.session.commit()
        return common_response_api(
            status_code=EnumStatus.SUCCESS,
            message="Job description created successfully",
            data=[{"job_id": job.id, "job_code": job_code}],
            errors=[],
        )
    except Exception as e:
        db.session.rollback()
        return common_response_api(
            status_code=EnumStatus.INTERNAL_SERVER_ERROR,
            message="Failed to create job description",
            data=[],
            errors=[str(e)],
        )
    
#-------END----------------------------------------create_job_description_service------------------------------------------------END--#

#-------START----------------------------------------get_companie_info_service------------------------------------------------START--#
def get_companie_info_service(company_id):
    companies = Company.query.filter_by(company_id=company_id).all()
    data = []

    for company in companies:
        company_data = {
            "company_id": company.company_id,
            "company_name": company.company_name,
            "company_address": company.company_address,
            "company_email": company.company_email,
            "company_phone": company.company_phone,
            "branches": []
        }

        for branch in company.branches:
            branch_data = {
                "branch_id": branch.branch_id,
                "branch_name": branch.branch_name,
                "city": {
                    "city_id": branch.city.city_id,
                    "city_name": branch.city.city_name,
                    "country": {
                        "country_id": branch.city.country.country_id,
                        "country_name": branch.city.country.country_name,
                        "country_code": branch.city.country.country_code
                    }
                },
                "departments": []
            }

            for department in branch.departments:
                department_data = {
                    "department_id": department.department_id,
                    "department_name": department.department_name,
                    "projects": []
                }

                for project in department.projects:
                    project_data = {
                        "project_id": project.project_id,
                        "project_name": project.project_name,
                        "managers": [
                            {
                                "manager_id": manager.manager_id,
                                "manager_name": manager.user.username,
                                "manager_user_id": manager.user_id
                            }
                            for manager in project.managers
                        ],
                     "job_descriptions" : [
                         {
                             "job_description_id": job.id,
                             "job_description": job.job_description,
                             "created_by": job.created_by,
                             "updated_by": job.updated_by,
                             "remarks": job.remarks,
                             "is_active": job.is_active
                         }
                         for job in project.job_descriptions
                     ]
                    }
                    department_data["projects"].append(project_data)

                branch_data["departments"].append(department_data)

            company_data["branches"].append(branch_data)

        data.append(company_data)
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="Companies fetched successfully",
        data=[{"companies": data}],
        errors=[],
    )
#-------END----------------------------------------get_companie_info_service------------------------------------------------END--#


#-------START----------------------------------------get_all_companies_service------------------------------------------------START--#

def get_all_companies_service():
    companies = Company.query.all()
    data = []

    for company in companies:
        company_data = {
            "company_id": company.company_id,
            "company_name": company.company_name,
            "company_address": company.company_address,
            "company_email": company.company_email,
            "company_phone": company.company_phone,
            "branches": []
        }

        for branch in company.branches:
            branch_data = {
                "branch_id": branch.branch_id,
                "branch_name": branch.branch_name,
                "city": {
                    "city_id": branch.city.city_id,
                    "city_name": branch.city.city_name,
                    "country": {
                        "country_id": branch.city.country.country_id,
                        "country_name": branch.city.country.country_name,
                        "country_code": branch.city.country.country_code
                    }
                },
                "departments": []
            }

            for department in branch.departments:
                department_data = {
                    "department_id": department.department_id,
                    "department_name": department.department_name,
                    "projects": []
                }

                for project in department.projects:
                    project_data = {
                        "project_id": project.project_id,
                        "project_name": project.project_name,
                        "managers": [
                            {
                                "manager_id": manager.manager_id,
                                "manager_name": manager.user.username,
                                "manager_user_id": manager.user_id

                            }
                            for manager in project.managers
                        ]
                    }
                    department_data["projects"].append(project_data)

                branch_data["departments"].append(department_data)

            company_data["branches"].append(branch_data)

        data.append(company_data)
    return common_response_api(
        status_code=EnumStatus.SUCCESS,
        message="Companies fetched successfully",
        data=[{"companies": data}],
        errors=[],
    )
#-------END----------------------------------------get_all_companies_service------------------------------------------------END--#