from flask_login import UserMixin
from extensions import db

class Notification_linkage(db.Model,UserMixin):
    not_id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(100), nullable=False)
    to_user = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
   


class Notification(db.Model,UserMixin):
    notification_id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
