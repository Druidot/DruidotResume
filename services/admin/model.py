from flask_login import UserMixin
from extensions import db

class Customer(db.Model,UserMixin):
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

    branches = db.relationship('Branch', backref='company', lazy=True)

# Country Table
class Country(db.Model):
    __tablename__ = 'country_mst'
    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_name = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(10), unique=True)

    cities = db.relationship('City', backref='country', lazy=True)

# City Table
class City(db.Model):
    __tablename__ = 'city_mst'
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(255), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country_mst.country_id'))

    branches = db.relationship('Branch', backref='city', lazy=True)

# Branch Table
class Branch(db.Model):
    __tablename__ = 'branch_mst'
    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_name = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_mst.company_id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city_mst.city_id'), nullable=False)

    departments = db.relationship('Department', backref='branch', lazy=True)

# Department Table
class Department(db.Model):
    __tablename__ = 'department_mst'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(255), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch_mst.branch_id'), nullable=False)

    projects = db.relationship('Project', backref='department', lazy=True)

# Project Table
class Project(db.Model):
    __tablename__ = 'project_mst'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department_mst.department_id'), nullable=False)

    managers = db.relationship('Manager', secondary='manager_project_map', back_populates='projects')
    job_descriptions = db.relationship('ManagerJobdescriptionModel', backref='projects', lazy=True)

# Manager Table
class Manager(db.Model):
    __tablename__ = 'manager_mst'

    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    manager_name = db.Column(db.String(255), nullable=False)

    # Relationship with User model
    user = db.relationship('User', backref=db.backref('manager', uselist=False))

    # Relationship with Project through association table 'manager_project_map'
    projects = db.relationship('Project', secondary='manager_project_map', back_populates='managers')

# Many-to-Many Relationship: Manager ↔ Project
class ManagerProjectMapModel(db.Model):
    __tablename__ = 'manager_project_map'
    manager_id = db.Column(db.Integer, db.ForeignKey('manager_mst.manager_id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_mst.project_id'), primary_key=True)

    manager = db.relationship('Manager', backref='manager_project_maps')
    project = db.relationship('Project', backref='project_manager_maps')





class ManagerJobdescriptionModel(db.Model):
    __tablename__ = 'manager_project_job_map'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project_mst.project_id'), primary_key=True)

    job_description = db.Column(db.Text, nullable=False)
    
    # New columns
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Status flag
    created_dt = db.Column(db.DateTime, default=db.func.now(), nullable=False)  # Creation timestamp
    updated_dt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)  # Last update timestamp
    created_by = db.Column(db.String(50), nullable=True)  # Creator's identifier (e.g., username)
    updated_by = db.Column(db.String(50), nullable=True)  # Last updater's identifier
    remarks = db.Column(db.String(255), nullable=True)  # Additional notes or comments

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




   

