from datetime import datetime
import random
import uuid
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from services.admin.model import Branch, City, Company, Country, Department, Manager, ManagerJobdescriptionModel, ManagerProjectMapModel, Project
from services.admin.service import change_role_service, create_job_description_service, get_all_companies_service, get_branch_by_city_service, get_city_by_company_service, get_companie_info_service, get_department_by_branch_service, get_manager_by_project_service, get_manager_project_job_map_service, get_project_by_department_service, get_records_service, make_activate_service, make_admin_service, make_verified_service
from services.login_and_registration.model import User
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========== ADMIN ROUTES (HTML) =========== #

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

@admin_bp.route('/delete_company/<int:company_id>', methods=['GET'])
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)

    db.session.delete(company)
    db.session.commit()

    flash("Company deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/update_company/<int:company_id>', methods=['POST'])
def update_company(company_id):
    company = Company.query.get_or_404(company_id)

    # Update fields from form data
    company.company_name = request.form['company_name']
    company.company_address = request.form['company_address']
    company.company_email = request.form['company_email']
    company.company_phone = request.form['company_phone']

    db.session.commit()

    flash("Company updated successfully!", "success")
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

@admin_bp.route('/update_country/<int:country_id>', methods=['POST'])
def update_country(country_id):
    country = Country.query.get_or_404(country_id)

    # Update fields from form data
    country.country_name = request.form['country_name']
    country.country_code = request.form['country_code']

    db.session.commit()

    flash("Country updated successfully!", "success")
    return redirect(url_for('auth.dashboard'))

@admin_bp.route('/delete_country/<int:country_id>', methods=['GET'])
def delete_country(country_id):
    country = Country.query.get_or_404(country_id)
    db.session.delete(country)
    db.session.commit()
    
    flash("Country deleted successfully!", "success")
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

@admin_bp.route('/delete_city/<int:city_id>', methods=['GET'])
def delete_city(city_id):
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    
    flash("City deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/update_city/<int:city_id>', methods=['POST'])
def update_city(city_id):
    city = City.query.get_or_404(city_id)

    # Update fields from form data
    city.city_name = request.form['city_name']
    city.country_id = request.form['city_country']

    db.session.commit()

    flash("City updated successfully!", "success")
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

@admin_bp.route('/delete_branch/<int:branch_id>', methods=['GET'])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    
    flash("Branch deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/update_branch/<int:branch_id>', methods=['POST'])
def update_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)

    # Update fields from form data
    branch.branch_name = request.form['branch_name']
    branch.company_id = request.form['company_id']
    branch.city_id = request.form['city_id']

    db.session.commit()

    flash("Branch updated successfully!", "success")
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

@admin_bp.route('/delete_department/<int:department_id>', methods=['GET'])
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    
    flash("Department deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/update_department/<int:department_id>', methods=['POST'])
def update_department(department_id):
    department = Department.query.get_or_404(department_id)

    # Update fields from form data
    department.department_name = request.form['department_name']
    department.branch_id = request.form['branch_id']

    db.session.commit()

    flash("Department updated successfully!", "success")
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

@admin_bp.route('/delete_project/<int:project_id>', methods=['GET'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    
    flash("Project deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/update_project/<int:project_id>', methods=['POST'])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Update fields from form data
    project.project_name = request.form['project_name']
    project.department_id = request.form['department_id']

    db.session.commit()

    flash("Project updated successfully!", "success")
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

@admin_bp.route('/delete_manager/<int:manager_id>', methods=['GET'])
def delete_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    db.session.delete(manager)
    db.session.commit()
    
    flash("Manager deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


@admin_bp.route('/add_manager_project_map', methods=['POST'])
def manager_map_project():
    manager_id = request.form['manager_id']
    project_id = request.form['project_id']
    company_id = request.form['company_id']
    city_id = request.form['city_id']
    branch_id = request.form['branch_id']
    department_id = request.form['department_id']
    manager_map_project = ManagerProjectMapModel(manager_id=manager_id, project_id=project_id,company_id=company_id, city_id=city_id, branch_id=branch_id, department_id=department_id)
    db.session.add(manager_map_project)
    db.session.commit()
    flash("Manager added successfully!", "success")
    return redirect(url_for('auth.dashboard'))

@admin_bp.route('/delete_manager_project_map/<int:manager_project_map_id>', methods=['GET'])
def delete_manager_project_map(manager_project_map_id):
    manager_project_map = ManagerProjectMapModel.query.get_or_404(manager_project_map_id)
    db.session.delete(manager_project_map)
    db.session.commit()
    
    flash("Manager-Project Mapping deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))


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




# =========== ADMIN ROUTES (APIS) =========== #

@admin_bp.route("/make_admin", methods=["POST"])
def make_admin():
    data = request.get_json()
    return make_admin_service(data)
   

@admin_bp.route("/make_activate", methods=["POST"])
def make_active():
    data = request.get_json()
    return make_activate_service(data)


    
@admin_bp.route("/make_verified", methods=["POST"])
def make_verified():
    data = request.get_json()
    return make_verified_service(data)



@admin_bp.route("/change_role", methods=["POST"])
def change_role():
    data = request.get_json()
    return change_role_service(data)




# Update any record dynamically


# =========== GET ALL RECORDS (API) =========== #
@admin_bp.route('/get_records/<table>')
def get_records(table):
   return get_records_service(table)


@admin_bp.route('/get_all_records', methods=['GET'])
def all_get_companies():
    return get_all_companies_service()
   

@admin_bp.route('/get_all_records/<int:company_id>', methods=['GET'])
def get_companie_info(company_id):
    return get_companie_info_service(company_id)
   

@admin_bp.route('/company/details/<int:company_id>', methods=['GET'])
@login_required
def get_company_details(company_id):
    company_detail= Company.query.filter_by(company_id=company_id).first()
    # return render_template('./frontend/company_details.html',company_id=company_id,company_detail=company_detail)
    return render_template('./screens/company_page.html',company_id=company_id,company_detail=company_detail)





@admin_bp.route('/add/job-description', methods=['POST'])
@login_required
def create_job_description():
    data = request.json
    return create_job_description_service(data)

    


@admin_bp.route('/get_records/city_by_company/<company_id>', methods=['GET'])
def get_city_by_company(company_id):
    return get_city_by_company_service(company_id)



    
@admin_bp.route('/get_records/branch_by_city/<city_id>/<company_id>', methods=['GET'])
def get_branch_by_city(city_id,company_id):
    return get_branch_by_city_service(city_id,company_id)
   

@admin_bp.route('/get_records/department_by_branch/<branch_id>', methods=['GET'])
def get_department_by_branch(branch_id):
    return get_department_by_branch_service(branch_id)
  

@admin_bp.route('/get_records/project_by_department/<department_id>', methods=['GET'])
def get_project_by_department(department_id):
    return get_project_by_department_service(department_id)
   

@admin_bp.route('/get_records/manager_by_project/<project_id>', methods=['GET'])
def get_manager_by_project(project_id):
    return get_manager_by_project_service(project_id)
  

@admin_bp.route('/get_records/manager_project_job_map', methods=['GET'])
def get_manager_project_job_map():
    company_id = request.args.get('company_id', type=int)
    city_id = request.args.get('city_id', type=int)
    branch_id = request.args.get('branch_id', type=int)
    department_id = request.args.get('department_id', type=int)
    project_id = request.args.get('project_id', type=int)
    return get_manager_project_job_map_service(company_id=company_id, city_id=city_id, branch_id=branch_id, department_id=department_id, project_id=project_id)
   
@admin_bp.route('/help_page', methods=['GET'])
@login_required
def help_page():
    if current_user.is_admin:
        return render_template('./common_components/Admin_help.html')   
    else:
        return render_template('./common_components/user_help.html')
