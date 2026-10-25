# LearnHub — Online Learning Platform

A full-stack learning platform starter built with Flask, SQLAlchemy, SQLite (default) and optional MySQL. Includes course discovery/search, account registration/login, student dashboard, course enrollment, lesson progress tracking, and an admin course-creation page.

## Features

- Responsive course catalogue with search and category filter
- Course detail pages and lesson lists
- Student registration and login with hashed passwords
- Enroll in courses and view a personal dashboard
- Mark lessons complete and track progress
- Admin dashboard and course creation
- SQLite default for easy local setup; optional MySQL configuration
- Seed script with sample courses and a demo admin account

  ## 🌟 Advantages of LearnHub

LearnHub is designed to provide a simple and organized online learning experience. The project demonstrates how web technologies can be combined to create a learning platform.

- **📚 Centralized Learning:** Provides a single platform where users can access learning materials and course-related information.
- **🖥️ User-Friendly Interface:** Uses HTML and CSS to present content in a clear and organized layout.
- **🔐 User Account Management:** Supports account-related functionality, including registration and login, according to the application's implementation.
- **📖 Course Access:** Helps learners browse courses and access course pages through the web interface.
- **⚙️ Backend Integration:** Uses Python and Flask to handle application logic and web requests.
- **🗄️ Database Management:** Uses SQLite to store and manage application data.
- **📱 Interactive Experience:** Uses JavaScript to support frontend interactions where implemented.
- **🧩 Modular Structure:** Separates application logic, templates, static assets, and database-related files to make the code easier to understand and maintain.
- **💰 Cost-Effective Development:** Uses widely available development tools and technologies, making the project suitable for learning and experimentation.
- **🚀 Expandable Project:** Can be extended with additional features, such as quizzes, course progress tracking, certificates, notifications, and more.

### 🎯 Learning Outcomes

Developing LearnHub helped me gain practical experience with:

- Python and Flask web development
- Frontend and backend integration
- SQLite database operations
- HTML, CSS, and JavaScript
- Git and GitHub for version control
- Debugging, problem-solving, and project organization

### 🔮 Future Enhancements

Possible future improvements include:

- Adding video lessons and downloadable learning resources
- Implementing quizzes and assessments
- Tracking learner progress and course completion
- Adding course reviews and ratings
- Improving accessibility and mobile responsiveness
- Deploying the application online for public access

*Note: Future enhancements are planned possibilities and may not be available in the current version.*

## Requirements

- Python 3.10+
- Windows 10/11
- Internet connection for externally hosted course-card images (optional)

## Windows setup (PowerShell)

```powershell
# 1. Extract the ZIP and open the project folder in VS Code
cd learnhub_platform

# 2. Create and activate a virtual environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# If PowerShell blocks activation, use Command Prompt instead:
# .venv\Scripts\activate.bat

# 3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Add sample courses and demo admin
python seed.py

# 5. Start the development server
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Demo admin

- Email: `admin@learnhub.local`
- Password: `ChangeMe123!`

This is a local demo credential. Change it before any deployment and do not publish real secrets.

## MySQL option

The project uses SQLite by default, so MySQL is not required to get started. To use MySQL:

1. Create a MySQL database and user, then run `schema.sql` in MySQL Workbench.
2. Install a MySQL driver: `pip install PyMySQL`.
3. Set the environment variable in PowerShell before running the app:

```powershell
$env:DATABASE_URL = "mysql+pymysql://learnhub_user:YOUR_PASSWORD@localhost/learnhub"
python seed.py
python app.py
```

Use URL-encoded credentials if your password contains special characters. Never commit database passwords or `.env` files.

## Folder structure

```text
learnhub_platform/
├── app.py
├── seed.py
├── requirements.txt
├── schema.sql
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── course.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── learn.html
│   ├── admin.html
│   ├── course_form.html
│   └── 404.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Routes

| Route | Purpose |
|---|---|
| `/` | Browse and search courses |
| `/course/<slug>` | Course details |
| `/register` | Create student account |
| `/login` | Sign in |
| `/dashboard` | Student dashboard |
| `/enroll/<course_id>` | Enroll in a course |
| `/learn/<course_id>` | Lesson player and progress |
| `/lesson/<lesson_id>/complete` | Progress API |
| `/admin` | Admin dashboard |
| `/admin/courses/new` | Add a course and lessons |

## Before production deployment

This is an educational starter, not a production-audited LMS. Before deploying publicly, set a strong secret key, disable Flask debug mode, add CSRF protection and rate limiting, use database migrations, validate uploaded media, implement email verification/password reset, add automated tests, and use HTTPS. Do not put sensitive student data in a public repository.
