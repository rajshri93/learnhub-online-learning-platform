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
