from flask_login import UserMixin
from extensions import db

# ManagerProjectMapModel (Many-to-Many relationship between Manager and Project)
class ManagerProjectMapModel(db.Model):
    __tablename__ = 'manager_project_map'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_mst.company_id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city_mst.city_id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch_mst.branch_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department_mst.department_id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager_mst.manager_id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project_mst.project_id'))

    manager = db.relationship('Manager', backref=db.backref('manager_project_maps', cascade="all, delete"))
    project = db.relationship('Project', backref=db.backref('project_manager_maps', cascade="all, delete"))
    city = db.relationship('City', backref=db.backref('project_manager_maps', cascade="all, delete"))
    branch = db.relationship('Branch', backref=db.backref('project_manager_maps', cascade="all, delete"))
    department = db.relationship('Department', backref=db.backref('project_manager_maps', cascade="all, delete"))
    company = db.relationship('Company', backref=db.backref('project_manager_maps', cascade="all, delete"))

# ManagerJobdescriptionModel
class ManagerJobdescriptionModel(db.Model):
    __tablename__ = 'manager_project_job_map'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(255), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)  # e.g., 'Full-time', 'Part-time', 'Contract'
    job_location = db.Column(db.String(255), nullable=False)  # Location of the job
    job_code = db.Column(db.String(50), nullable=False)  # Unique job code or identifier
    job_start_date = db.Column(db.Date, nullable=False)  # Start date of the job
    job_end_date = db.Column(db.Date, nullable=True)  # End date of the job (if applicable)
    
    manager_id = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_mst.company_id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city_mst.city_id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch_mst.branch_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department_mst.department_id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project_mst.project_id', ondelete='CASCADE'), nullable=False)

    job_description = db.Column(db.Text, nullable=False)

    project = db.relationship('Project', backref=db.backref('manager_project_job_map', cascade="all, delete"))
    city = db.relationship('City', backref=db.backref('manager_project_job_map', cascade="all, delete"))
    branch = db.relationship('Branch', backref=db.backref('manager_project_job_map', cascade="all, delete"))
    department = db.relationship('Department', backref=db.backref('manager_project_job_map', cascade="all, delete"))
    company = db.relationship('Company', backref=db.backref('manager_project_job_map', cascade="all, delete"))
    
    # New columns
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Status flag
    created_dt = db.Column(db.DateTime, default=db.func.now(), nullable=False)  # Creation timestamp
    updated_dt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)  # Last update timestamp
    created_by = db.Column(db.String(50), nullable=True)  # Creator's identifier (e.g., username)
    updated_by = db.Column(db.String(50), nullable=True)  # Last updater's identifier
    resume_process_count = db.Column(db.Integer, default=0)  # Count of resumes processed for this job description
    resume_shortlist_count = db.Column(db.Integer, default=0)  # Count of resumes shortlisted for this job description
    remarks = db.Column(db.Text, nullable=True)  # Additional remarks or comments


    # Composite Foreign Key
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['manager_id', 'project_id'],
            ['manager_project_map.manager_id', 'manager_project_map.project_id']
        ),
    )

    # Relationship with ManagerProjectMapModel
    manager_project_map = db.relationship('ManagerProjectMapModel', backref='job_descriptions')
    project = db.relationship('Project', backref='manager_project_job_maps')


# Customer Table
class Customer(db.Model, UserMixin):
    cust_id = db.Column(db.Integer, primary_key=True)
    comapny_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    manager_name = db.Column(db.String(100), nullable=False)
    manager_email = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Company Table
class Company(db.Model):
    __tablename__ = 'company_mst'
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.String(500))
    company_email = db.Column(db.String(255), unique=True)
    company_phone = db.Column(db.String(20))

    branches = db.relationship('Branch', backref='company', lazy=True, cascade="all, delete")

# Country Table
class Country(db.Model):
    __tablename__ = 'country_mst'
    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_name = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(10), unique=True)
    cities = db.relationship('City', backref='country', lazy=True, cascade="all, delete")

# City Table
class City(db.Model):
    __tablename__ = 'city_mst'
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(255), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country_mst.country_id'))
    branches = db.relationship('Branch', backref='city', lazy=True, cascade="all, delete")

# Branch Table
class Branch(db.Model):
    __tablename__ = 'branch_mst'
    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_name = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_mst.company_id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city_mst.city_id'), nullable=False)
    departments = db.relationship('Department', backref='branch', lazy=True, cascade="all, delete")

# Department Table
class Department(db.Model):
    __tablename__ = 'department_mst'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(255), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch_mst.branch_id'), nullable=False)

    projects = db.relationship('Project', backref='department', lazy=True, cascade="all, delete")

# Project Table
class Project(db.Model):
    __tablename__ = 'project_mst'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department_mst.department_id'), nullable=False)
    managers = db.relationship('Manager', secondary='manager_project_map', back_populates='projects', cascade="all, delete")
    job_descriptions = db.relationship('ManagerJobdescriptionModel', backref='projects', lazy=True, cascade="all, delete")

# Manager Table
class Manager(db.Model):
    __tablename__ = 'manager_mst'
    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    manager_name = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_mst.company_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('manager', uselist=False))
    projects = db.relationship('Project', secondary='manager_project_map', back_populates='managers', cascade="all, delete")

# Organization Table
class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    logo_path = db.Column(db.Text, nullable=False)
    created_dt = db.Column(db.DateTime, default=db.func.now(), nullable=False)  # Creation timestamp
    updated_dt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)  # Last update timestamp
    created_by = db.Column(db.String(50), nullable=True)  # Creator's identifier (e.g., username)
    updated_by = db.Column(db.String(50), nullable=True)  # Last updater's identifier
    user = db.relationship('User', backref=db.backref('Organization', uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)




   

