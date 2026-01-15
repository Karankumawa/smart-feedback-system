from flask_mongoengine import MongoEngine
from flask_login import UserMixin
from datetime import datetime

db = MongoEngine()

class User(UserMixin, db.Document):
    username = db.StringField(max_length=150, unique=True, required=True)
    password_hash = db.StringField(max_length=150, required=True)
    role = db.StringField(max_length=50, required=True, default='User') # Guest, User, Admin
    
    # Verification Details
    full_name = db.StringField(max_length=150)
    organization = db.StringField(max_length=150)
    department = db.StringField(max_length=100)
    employee_id = db.StringField(max_length=50)
    is_verified = db.BooleanField(default=False)
    
    # Meta needed for UserMixin to work properly with MongoEngine if needed, 
    # but standard UserMixin works if 'id' is present. 
    # MongoEngine documents provide 'id' (ObjectId) automatically.

class Feedback(db.Document):
    content = db.StringField(required=True)
    sentiment_score = db.FloatField(required=True)
    sentiment_label = db.StringField(max_length=50, required=True) # Positive, Negative, Neutral
    timestamp = db.DateTimeField(default=datetime.utcnow)
    
    # Reference to User. In Relational -> ForeignKey. In Mongo -> ReferenceField
    user = db.ReferenceField(User)
