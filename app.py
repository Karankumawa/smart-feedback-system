from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Feedback
from analysis import analyze_sentiment
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_URI'),
    'connect': False  # Allow lazy connection
}

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# Create Admin if not exists - Karan
# We can't use app_context() quite the same way for create_all since Mongo is schemaless
# But checking for admin is fine.
with app.app_context():
    if not User.objects(username='karan').first():
        admin = User(username='karan', password_hash=generate_password_hash('karan'), role='Admin')
        admin.save()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            label, score = analyze_sentiment(content)
            user_instance = current_user if current_user.is_authenticated else None
            
            # Create feedback
            # If user is None, field is nullable/optional in model?
            # In ReferenceField, if we pass None, it should work if it's not required.
            # In models.py we didn't set required=True for user.
            
            feedback = Feedback(content=content, sentiment_score=score, sentiment_label=label)
            if user_instance:
                feedback.user = user_instance
            
            feedback.save()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.objects(username=username).first()
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
        
        if User.objects(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('register'))
            
        organization = request.form.get('organization')
        new_user = User(username=username, password_hash=hashed_password, role='User', organization=organization)
        new_user.save()
        flash('Account created! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', register_mode=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Incorrect current password', 'danger')
            return redirect(url_for('change_password'))
            
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('change_password'))
            
        current_user.password_hash = generate_password_hash(new_password)
        current_user.save()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('change_password.html')

@app.route('/admin/user/<user_id>/update', methods=['GET', 'POST'])
@login_required
def admin_update_user(user_id):
    if current_user.role != 'Admin':
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
        
    user = User.objects(pk=user_id).first_or_404()
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.department = request.form.get('department')
        user.organization = request.form.get('organization')
        user.employee_id = request.form.get('employee_id')
        user.save()
        flash('User details updated successfully', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('edit_user.html', user=user)

@app.route('/dashboard')
@login_required
def dashboard():
    sort_by = request.args.get('sort_by', 'timestamp')
    all_users = []
    
    if current_user.role == 'Admin':
        feedbacks = Feedback.objects.order_by('-timestamp')
        
        if sort_by == 'organization':
            all_users = User.objects.order_by('organization')
        elif sort_by == 'employee_id':
             all_users = User.objects.order_by('employee_id')
        else:
            all_users = User.objects.all()
    else:
        feedbacks = Feedback.objects(user=current_user).order_by('-timestamp')
    return render_template('dashboard.html', feedbacks=feedbacks, all_users=all_users, sort_by=sort_by)

@app.route('/verify-profile', methods=['GET', 'POST'])
@login_required
def verify_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.department = request.form.get('department')
        current_user.organization = request.form.get('organization')
        current_user.employee_id = request.form.get('employee_id')
        current_user.is_verified = True
        
        current_user.save()
        flash('Profile details updated successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('verify_profile.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/api/stats')
def get_stats():
    # Public stats or protected? Let's make it public for simplicity or protected
    feedbacks = Feedback.objects.all()

    # Using pymongo/mongoengine logic, better to do aggregation but python list comp is fine for small scale
    positive = feedbacks.filter(sentiment_label='Positive').count()
    neutral = feedbacks.filter(sentiment_label='Neutral').count()
    negative = feedbacks.filter(sentiment_label='Negative').count()
    
    return jsonify({
        'labels': ['Positive', 'Neutral', 'Negative'],
        'data': [positive, neutral, negative]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
