from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Feedback
from analysis import analyze_sentiment
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    # Create Admin - Karan
    if not User.query.filter_by(username='karan').first():
        admin = User(username='karan', password_hash=generate_password_hash('karan'), role='Admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            label, score = analyze_sentiment(content)
            user_id = current_user.id if current_user.is_authenticated else None
            feedback = Feedback(content=content, sentiment_score=score, sentiment_label=label, user_id=user_id)
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('register'))
            
        new_user = User(username=username, password_hash=hashed_password, role='User')
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', register_mode=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    all_users = []
    if current_user.role == 'Admin':
        feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
        all_users = User.query.all()
    else:
        feedbacks = Feedback.query.filter_by(user_id=current_user.id).order_by(Feedback.timestamp.desc()).all()
    return render_template('dashboard.html', feedbacks=feedbacks, all_users=all_users)

@app.route('/verify-profile', methods=['GET', 'POST'])
@login_required
def verify_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.department = request.form.get('department')
        current_user.employee_id = request.form.get('employee_id')
        current_user.is_verified = True
        
        db.session.commit()
        flash('Profile details updated successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('verify_profile.html')

@app.route('/api/stats')
def get_stats():
    # Public stats or protected? Let's make it public for simplicity or protected
    # Let's verify if user is authenticated for real app, but for now open
    # Aggregate data
    if current_user.is_authenticated and current_user.role == 'Admin':
         feedbacks = Feedback.query.all()
    else:
         # Guests/Users might only see their own or global trends? Let's show global trends
         feedbacks = Feedback.query.all() 

    positive = len([f for f in feedbacks if f.sentiment_label == 'Positive'])
    neutral = len([f for f in feedbacks if f.sentiment_label == 'Neutral'])
    negative = len([f for f in feedbacks if f.sentiment_label == 'Negative'])
    
    return jsonify({
        'labels': ['Positive', 'Neutral', 'Negative'],
        'data': [positive, neutral, negative]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
