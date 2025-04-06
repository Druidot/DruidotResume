from datetime import datetime
import random
import uuid
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from services.admin.model import Branch, City, Company, Country, Department, Manager, ManagerJobdescriptionModel, ManagerProjectMapModel, Project
from services.login_and_registration.model import User
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/make_admin", methods=["POST"])
def make_admin():
    data = request.get_json()
    print("data=>", data)

    user_data = User.query.get(data["user_id"])  # Fetch user by ID
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    if user_data.is_admin:
        user_data.is_admin = False
        db.session.commit()  # Commit the change
        return jsonify({"message": "User is now not an admin"})

    user_data.is_admin = True
    db.session.commit()  # Commit the change
    return jsonify({"message": "User is now an admin"})



@admin_bp.route("/make_activate", methods=["POST"])
def make_active():
    data = request.get_json()

    user_data = User.query.get(data["user_id"])  # Fetch user by ID
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    if user_data.is_active:
        user_data.is_active = False
        db.session.commit()  # Commit the change
        return jsonify({"message": "User is now inactive"})

    user_data.is_active = True
    db.session.commit()  # Commit the change
    return jsonify({"message": "User is now active"})


@admin_bp.route("/make_verified", methods=["POST"])
def make_verified():
    data = request.get_json()

    user_data = User.query.get(data["user_id"])  # Fetch user by ID
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    if user_data.is_verified:
        user_data.is_verified = False
        db.session.commit()  # Commit the change
        return jsonify({"message": "User is now not verified"})

    user_data.is_verified = True
    db.session.commit()  # Commit the change
    return jsonify({"message": "User is now verified"})



@admin_bp.route("/change_role", methods=["POST"])
def change_role():
    data = request.get_json()

    user_data = User.query.get(data["user_id"])  # Fetch user by ID
    if not user_data:
        return jsonify({"error": "User not found"}), 404

 
    user_data.roles = data.get("user_role")
    db.session.commit()  # Commit the change
    return jsonify({"message": "User role changed"})


   






@admin_bp.route('/add_company', methods=['POST'])
def add_company():
    print(request.form)
    name = request.form['company_name']
    address = request.form['company_address']
    email = request.form['company_email']
    phone = request.form['company_phone']

    company = Company(company_name=name, company_address=address, company_email=email, company_phone=phone)
    db.session.add(company)
    db.session.commit()

    flash("Company added successfully!", "success")
    return redirect(url_for('auth.dashboard'))

# 2️⃣ Add Country
@admin_bp.route('/add_country', methods=['POST'])
def add_country():
    name = request.form['country_name']
    code = request.form['country_code']

    country = Country(country_name=name, country_code=code)
    db.session.add(country)
    db.session.commit()

    flash("Country added successfully!", "success")
    return redirect(url_for('auth.dashboard'))


# 3️⃣ Add City
@admin_bp.route('/add_city', methods=['POST'])
def add_city():
    name = request.form['city_name']
    country_id = request.form['city_country']

    city = City(city_name=name, country_id=country_id)
    db.session.add(city)
    db.session.commit()

    flash("City added successfully!", "success")
    return redirect(url_for('auth.dashboard'))

# 4️⃣ Add Branch
@admin_bp.route('/add_branch', methods=['POST'])
def add_branch():
    name = request.form['branch_name']
    company_id = request.form['company_id']
    city_id = request.form['city_id']

    branch = Branch(branch_name=name, company_id=company_id, city_id=city_id)
    db.session.add(branch)
    db.session.commit()

    flash("Branch added successfully!", "success")
    return redirect(url_for('auth.dashboard'))

# 5️⃣ Add Department
@admin_bp.route('/add_department', methods=['POST'])
def add_department():
    name = request.form['department_name']
    branch_id = request.form['branch_id']

    department = Department(department_name=name, branch_id=branch_id)
    db.session.add(department)
    db.session.commit()

    flash("Department added successfully!", "success")
    return redirect(url_for('auth.dashboard'))

# 6️⃣ Add Project
@admin_bp.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['project_name']
    department_id = request.form['department_id']

    project = Project(project_name=name, department_id=department_id)
    db.session.add(project)
    db.session.commit()

    flash("Project added successfully!", "success")
    return redirect(url_for('auth.dashboard'))

# 7️⃣ Add Manager
@admin_bp.route('/add_manager', methods=['POST'])
def add_manager():
    company_id = request.form['company_id']
    manager_user_id = request.form['manager_user_id']

    manager = Manager(manager_name='',user_id=manager_user_id,company_id=company_id)
    db.session.add(manager)
    db.session.commit()

    flash("Manager added successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/add_manager_project_map', methods=['POST'])
def manager_map_project():
    manager_id = request.form['manager_id']
    project_id = request.form['project_id']
    company_id = request.form['company_id']
    city_id = request.form['city_id']
    branch_id = request.form['branch_id']
    department_id = request.form['department_id']




    # user_manager_id = request.form['user_manager_id']


    manager_map_project = ManagerProjectMapModel(manager_id=manager_id, project_id=project_id,company_id=company_id, city_id=city_id, branch_id=branch_id, department_id=department_id)
    db.session.add(manager_map_project)
    db.session.commit()

    flash("Manager added successfully!", "success")
    return redirect(url_for('auth.dashboard'))


# =========== DELETE ROUTES =========== #

# Delete any record dynamically
@admin_bp.route('/delete/<table>/<int:id>')
def delete_record(table, id):
    model_map = {
        'company': Company,
        'country': Country,
        'city': City,
        'branch': Branch,
        'department': Department,
        'project': Project,
        'manager': Manager
    }

    model = model_map.get(table)
    if not model:
        flash("Invalid table name!", "danger")
        return redirect(url_for('index'))

    record = model.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
        flash(f"{table.capitalize()} deleted successfully!", "success")
    else:
        flash(f"{table.capitalize()} not found!", "danger")

    return redirect(url_for('index'))

# =========== UPDATE ROUTES =========== #

# Update any record dynamically
@admin_bp.route('/update/<table>/<int:id>', methods=['POST'])
def update_record(table, id):
    model_map = {
        'company': Company,
        'country': Country,
        'city': City,
        'branch': Branch,
        'department': Department,
        'project': Project,
        'manager': Manager
    }

    model = model_map.get(table)
    if not model:
        flash("Invalid table name!", "danger")
        return redirect(url_for('index'))

    record = model.query.get(id)
    if not record:
        flash(f"{table.capitalize()} not found!", "danger")
        return redirect(url_for('index'))

    # Updating fields dynamically
    for key, value in request.form.items():
        setattr(record, key, value)

    db.session.commit()
    flash(f"{table.capitalize()} updated successfully!", "success")

    return redirect(url_for('index'))

# =========== GET ALL RECORDS (API) =========== #
@admin_bp.route('/get_records/<table>')
def get_records(table):
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
        return jsonify({"error": "Invalid table name"}), 400

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

    return jsonify(result), 200





@admin_bp.route('/get_all_records', methods=['GET'])
def all_get_companies():
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

    return jsonify({"companies": data}), 200




@admin_bp.route('/get_all_records/<int:company_id>', methods=['GET'])
def get_companie_info(company_id):
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

    return jsonify({"companies": data}), 200

@admin_bp.route('/company/details/<int:company_id>', methods=['GET'])
@login_required
def get_company_details(company_id):
    company_detail= Company.query.filter_by(company_id=company_id).first()
    return render_template('./frontend/company_details.html',company_id=company_id,company_detail=company_detail)


def generate_job_code():
    return f"JOB-{uuid.uuid4().hex[:8].upper()}"

@admin_bp.route('/add/job-description', methods=['POST'])
@login_required
def create_job_description():
    data = request.json
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

        return jsonify({"message": "Job description created successfully!", "id": job.id,"job_code":job_code}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    


@admin_bp.route('/get_records/city_by_company/<company_id>', methods=['GET'])
def get_city_by_company(company_id):
    cities = Branch.query.filter_by(company_id=company_id).all()
    managers = Manager.query.filter_by(company_id=company_id).all()
    if not cities and not managers:
        return jsonify({"message": "No cities found for this company"}), 404
    
    city_list = [{"city_id": city.city_id, "city_name": city.city.city_name} for city in cities]
    manager_list = [{"manager_id": manager.manager_id, "manager_name": manager.user.username} for manager in managers]


    return jsonify({"city_list":city_list,"manager_list":manager_list}), 200

@admin_bp.route('/get_records/branch_by_city/<city_id>/<company_id>', methods=['GET'])
def get_branch_by_city(city_id,company_id):
    branches = Branch.query.filter_by(city_id=city_id, company_id=company_id).all()
    branch_list = [{"branch_id": branch.branch_id, "branch_name": branch.branch_name} for branch in branches]
    return jsonify(branch_list), 200

@admin_bp.route('/get_records/department_by_branch/<branch_id>', methods=['GET'])
def get_department_by_branch(branch_id):
    departments = Department.query.filter_by(branch_id=branch_id).all()
    department_list = [{"department_id": department.department_id, "department_name": department.department_name} for department in departments]
    return jsonify(department_list), 200

@admin_bp.route('/get_records/project_by_department/<department_id>', methods=['GET'])
def get_project_by_department(department_id):
    projects = Project.query.filter_by(department_id=department_id).all()
    project_list = [{"project_id": project.project_id, "project_name": project.project_name} for project in projects]
    return jsonify(project_list), 200

@admin_bp.route('/get_records/manager_by_project/<project_id>', methods=['GET'])
def get_manager_by_project(project_id):
    managers = ManagerProjectMapModel.query.filter_by(project_id=project_id).all()
    manager_list = [{"manager_id": manager.manager_id, "manager_name": manager.manager.user.username} for manager in managers]
    return jsonify(manager_list), 200

@admin_bp.route('/get_records/manager_project_job_map/<project_id>', methods=['GET'])
def get_manager_project_job_map(project_id):
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
            "job_end_date": job.job_end_date.strftime('%Y-%m-%d') if job.job_end_date else None
        }
        for job in job_descriptions
    ]
    if not job_description_list:
        return jsonify({"message": "No job descriptions found for this project"}), 404
    return jsonify(job_description_list), 200