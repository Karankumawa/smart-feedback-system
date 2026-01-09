from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='User') # Guest, User, Admin
    
    # Verification Details
    full_name = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    employee_id = db.Column(db.String(50), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)
    sentiment_label = db.Column(db.String(50), nullable=False) # Positive, Negative, Neutral
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for Guest
    
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
