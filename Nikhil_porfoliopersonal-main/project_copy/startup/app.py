from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Use environment variable with fallback
app.config['API_KEY'] = os.getenv('API_KEY')  # Your API key from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careerpilot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    resumes = db.relationship('Resume', backref='user', lazy=True)
    applications = db.relationship('JobApplication', backref='user', lazy=True)
    quiz_scores = db.relationship('QuizScore', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    format = db.Column(db.String(20), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('JobApplication', backref='job', lazy=True)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)

class QuizCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    question_count = db.Column(db.Integer, default=0)

class QuizScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('quiz_category.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    applications = JobApplication.query.filter_by(user_id=current_user.id).all()
    quiz_scores = QuizScore.query.filter_by(user_id=current_user.id).all()
    
    # Calculate career progress
    career_progress = 0
    if quiz_scores:
        career_progress = sum(score.score for score in quiz_scores) / len(quiz_scores)
    
    return render_template('dashboard.html',
                         resumes=resumes,
                         applications=applications,
                         quiz_score=career_progress,
                         career_progress=career_progress)

@app.route('/resume-builder')
@login_required
def resume_builder():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('resume_builder.html', resumes=resumes)

@app.route('/career-guidance')
@login_required
def career_guidance():
    # Get recommended paths based on user's skills and interests
    recommended_paths = [
        {
            'title': 'Software Development',
            'description': 'Build and maintain software applications',
            'match_percentage': 85
        },
        {
            'title': 'Data Science',
            'description': 'Analyze and interpret complex data sets',
            'match_percentage': 75
        }
    ]
    
    # Get recommended skills
    recommended_skills = [
        {
            'name': 'Python Programming',
            'description': 'Core programming language for data science',
            'progress': 60
        },
        {
            'name': 'Machine Learning',
            'description': 'Build and train ML models',
            'progress': 40
        }
    ]
    
    return render_template('career_guidance.html',
                         recommended_paths=recommended_paths,
                         recommended_skills=recommended_skills)

@app.route('/job-portal')
@login_required
def job_portal():
    jobs = Job.query.all()
    saved_jobs = Job.query.join(JobApplication).filter(
        JobApplication.user_id == current_user.id,
        JobApplication.status == 'saved'
    ).all()
    
    return render_template('job_portal.html', jobs=jobs, saved_jobs=saved_jobs)

@app.route('/quiz')
@login_required
def quiz():
    categories = QuizCategory.query.all()
    strengths = ['Problem Solving', 'Algorithm Design', 'Data Structures']
    improvement_areas = ['System Design', 'Database Optimization']
    recommendations = [
        {
            'title': 'Practice System Design',
            'description': 'Work on designing scalable systems'
        },
        {
            'title': 'Learn Database Optimization',
            'description': 'Study advanced database concepts'
        }
    ]
    
    return render_template('quiz.html',
                         categories=categories,
                         strengths=strengths,
                         improvement_areas=improvement_areas,
                         recommendations=recommendations)

# API Routes
@app.route('/api/resume', methods=['POST'])
@login_required
def create_resume():
    # Verify API key in headers
    api_key = request.headers.get('X-API-Key')
    if api_key != app.config['API_KEY']:
        return jsonify({'error': 'Invalid API key'}), 401
        
    data = request.json
    resume = Resume(
        title=data['title'],
        content=data['content'],
        format=data['format'],
        user_id=current_user.id
    )
    db.session.add(resume)
    db.session.commit()
    return jsonify({'id': resume.id})

@app.route('/api/job/<int:job_id>/apply', methods=['POST'])
@login_required
def apply_job(job_id):
    # Verify API key in headers
    api_key = request.headers.get('X-API-Key')
    if api_key != app.config['API_KEY']:
        return jsonify({'error': 'Invalid API key'}), 401
        
    application = JobApplication(
        user_id=current_user.id,
        job_id=job_id
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/api/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    # Verify API key in headers
    api_key = request.headers.get('X-API-Key')
    if api_key != app.config['API_KEY']:
        return jsonify({'error': 'Invalid API key'}), 401
        
    data = request.json
    score = QuizScore(
        user_id=current_user.id,
        category_id=data['category_id'],
        score=data['score']
    )
    db.session.add(score)
    db.session.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 