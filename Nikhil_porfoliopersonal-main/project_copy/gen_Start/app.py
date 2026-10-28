from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

# Handle proxy headers if behind a reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    resumes = db.relationship('Resume', backref='user', lazy=True)
    job_applications = db.relationship('JobApplication', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20), default='applied')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    salary_range = db.Column(db.String(50))
    job_type = db.Column(db.String(20))
    experience_level = db.Column(db.String(20))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('JobApplication', backref='job', lazy=True)

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
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(email=email, name=name)
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
    return render_template('dashboard.html')

@app.route('/resume-builder')
@login_required
def resume_builder():
    return render_template('resume-builder.html')

@app.route('/resume-analyzer')
@login_required
def resume_analyzer():
    return render_template('resume-analyzer.html')

@app.route('/api/analyze-resume', methods=['POST'])
@login_required
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    # Here you would implement the actual resume analysis logic
    # For now, we'll return a mock analysis
    analysis = {
        'score': 75,
        'strengths': ['Strong professional summary', 'Clear work experience'],
        'improvements': [
            'Add more quantifiable achievements',
            'Include a dedicated skills section',
            'Optimize for ATS keywords'
        ]
    }
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/api/jobs')
def get_jobs():
    # Get filter parameters
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('jobType', '')
    experience = request.args.get('experience', '')
    
    # Query jobs with filters
    query = Job.query
    
    if search:
        query = query.filter(Job.title.ilike(f'%{search}%') | Job.company.ilike(f'%{search}%'))
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if experience:
        query = query.filter(Job.experience_level == experience)
    
    jobs = query.order_by(Job.posted_at.desc()).all()
    
    # Format jobs for response
    jobs_data = [{
        'id': job.id,
        'title': job.title,
        'company_name': job.company,
        'company_logo': f'https://via.placeholder.com/48?text={job.company[0]}',
        'location': job.location,
        'type': job.job_type,
        'salary_range': job.salary_range,
        'experience_required': job.experience_level,
        'posted_time': '2 days ago'  # You would calculate this based on posted_at
    } for job in jobs]
    
    return jsonify({
        'success': True,
        'jobs': jobs_data
    })

@app.route('/ai-assistant')
@login_required
def ai_assistant():
    return render_template('ai-assistant.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'success': False, 'message': 'No message provided'})
    
    # Here you would implement the actual AI chat logic
    # For now, we'll return a mock response
    response = f"I understand you're asking about {message}. Let me help you with that..."
    
    return jsonify({
        'success': True,
        'response': response
    })

# Add a route to serve static files with proper caching headers
@app.route('/static/<path:filename>')
def serve_static(filename):
    response = send_from_directory(app.static_folder, filename)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# Add error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 