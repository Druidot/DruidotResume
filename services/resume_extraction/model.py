from extensions import db
class CandidateModel(db.Model):
    __tablename__ = 'candidate_information'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    experience_months = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=True)
    resume_file = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    certifications = db.Column(db.String(255), nullable=True)

    # Additional Info
    education_degree = db.Column(db.String(255), nullable=True)
    education_university = db.Column(db.String(255), nullable=True)
    education_duration = db.Column(db.String(255), nullable=True)
    education_grade = db.Column(db.String(50), nullable=True)

    project_title = db.Column(db.String(255), nullable=True)
    project_description = db.Column(db.Text, nullable=True)

    created_dt = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_dt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    candidate_status = db.Column(db.String(50), default="New",nullable=False)  # New, In Progress, Completed, Rejected
    candidate_selected = db.Column(db.Boolean, default=False)  # True if selected for the job

    # Relationship
    job_description_id = db.Column(db.Integer, db.ForeignKey('manager_project_job_map.id'), nullable=False)  # FK to ManagerJobdescriptionModel
    job_description = db.relationship('ManagerJobdescriptionModel', backref='candidates')

    def __repr__(self):
        return f"<Candidate {self.name} - {self.email}>"