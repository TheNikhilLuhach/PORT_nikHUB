# CareerPilot - Your AI-Powered Career Development Platform

CareerPilot is a comprehensive career development platform that helps job seekers, freelancers, and employers navigate their professional journey with AI-powered tools and features.

## 🌟 Features

### 1. AI Resume Builder
- Create ATS-friendly resumes with AI suggestions
- Real-time content optimization
- Multiple professional templates
- Export in various formats (PDF, DOCX)
- ATS score checking

### 2. Career Guidance
- AI-powered career counseling
- Personalized career path recommendations
- Skill gap analysis
- Industry trend insights
- Career transition guidance

### 3. Job Portal
- Curated job listings
- Freelance opportunities
- Company profiles
- Application tracking
- Job alerts and notifications

### 4. Technical Quiz
- UI/UX design assessment
- Skill evaluation tests
- Industry-specific quizzes
- Performance analytics
- Learning recommendations

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/careerpilot.git
cd careerpilot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📱 User Manual

### Registration and Login
1. **New User Registration**
   - Click "Sign Up" on the landing page
   - Fill in your details (name, email, password)
   - Choose your role (job seeker, employer, freelancer)
   - Accept terms and conditions
   - Click "Create Account"

2. **Login**
   - Enter your email and password
   - Click "Sign In"
   - Use "Remember Me" for faster login
   - Access "Forgot Password" if needed

### Dashboard
The dashboard provides quick access to all features:
- Resume Builder
- Career Guidance
- Job Portal
- Technical Quiz
- Profile Settings

### AI Resume Builder
1. **Create New Resume**
   - Click "New Resume" in the Resume Builder section
   - Choose a template
   - Fill in your information:
     - Personal Details
     - Work Experience
     - Education
     - Skills
     - Projects
   - Get AI suggestions for content improvement
   - Check ATS score
   - Download or share your resume

2. **Edit Existing Resume**
   - Select a saved resume
   - Make changes
   - Save updates
   - Generate new version

### Career Guidance
1. **AI Career Counselor**
   - Start a chat session
   - Ask career-related questions
   - Get personalized advice
   - Receive skill recommendations

2. **Career Path Analysis**
   - Input your current role
   - Specify target industry
   - Get detailed transition plan
   - View required skills and certifications

### Job Portal
1. **Job Search**
   - Use filters (location, salary, experience)
   - Save job searches
   - Set up job alerts
   - Apply directly through the platform

2. **Freelance Projects**
   - Browse available projects
   - Filter by category and budget
   - Submit proposals
   - Track application status

### Technical Quiz
1. **Take Assessment**
   - Select quiz category
   - Answer questions
   - Get immediate feedback
   - View detailed results

2. **Track Progress**
   - View quiz history
   - Check improvement areas
   - Get learning recommendations
   - Compare with industry standards

## 🔧 Technical Details

### Project Structure
```
careerpilot/
├── app.py              # Main application file
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Landing page
│   ├── login.html     # Login page
│   ├── register.html  # Registration page
│   └── ...
├── static/            # Static files
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── images/       # Image assets
└── instance/         # Instance-specific files
```

### Database Models
- User: Stores user information and authentication details
- Resume: Manages resume content and versions
- Job: Stores job listings and applications
- Quiz: Manages quiz questions and results

### Security Features
- Password hashing
- CSRF protection
- Session management
- Secure file uploads
- Input validation

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support
For support, email support@careerpilot.com or create an issue in the repository.

## 🙏 Acknowledgments
- Flask framework
- SQLAlchemy ORM
- OpenAI API
- All contributors and users 