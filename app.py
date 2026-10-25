import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-this-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///learnhub.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship("Enrollment", backref="student", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(40), nullable=False, default="Beginner")
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False, default="4 weeks")
    image_url = db.Column(db.String(500), nullable=True)
    featured = db.Column(db.Boolean, default=False)
    lessons = db.relationship("Lesson", backref="course", cascade="all, delete-orphan", order_by="Lesson.position")
    enrollments = db.relationship("Enrollment", backref="course", cascade="all, delete-orphan")

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    summary = db.Column(db.Text, nullable=False, default="")
    video_url = db.Column(db.String(500), nullable=True)
    position = db.Column(db.Integer, nullable=False, default=1)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_lessons = db.Column(db.Text, nullable=False, default="") # comma-separated lesson IDs for simple starter
    __table_args__ = (db.UniqueConstraint("user_id", "course_id", name="unique_student_course"),)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "info")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        user = db.session.get(User, session["user_id"])
        if not user or user.role != "admin":
            flash("Admin access is required.", "error")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_user():
    user = db.session.get(User, session["user_id"]) if session.get("user_id") else None
    return {"current_user": user}

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    query = Course.query
    if q:
        query = query.filter(db.or_(Course.title.ilike(f"%{q}%"), Course.description.ilike(f"%{q}%"), Course.instructor.ilike(f"%{q}%")))
    if category:
        query = query.filter_by(category=category)
    courses = query.order_by(Course.featured.desc(), Course.id.desc()).all()
    categories = [row[0] for row in db.session.query(Course.category).distinct().order_by(Course.category).all()]
    return render_template("index.html", courses=courses, categories=categories, q=q, selected_category=category)

@app.route("/course/<slug>")
def course_detail(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    enrolled = False
    if session.get("user_id"):
        enrolled = Enrollment.query.filter_by(user_id=session["user_id"], course_id=course.id).first() is not None
    return render_template("course.html", course=course, enrolled=enrolled)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter your name and email, and use a password with at least 8 characters.", "error")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "error")
            return render_template("register.html")
        user = User(name=name, email=email, role="student")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        flash("Account created. Welcome to LearnHub!", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            flash("Welcome back!", "success")
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/enroll/<int:course_id>", methods=["POST"])
@login_required
def enroll(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        flash("Course not found.", "error")
        return redirect(url_for("index"))
    existing = Enrollment.query.filter_by(user_id=session["user_id"], course_id=course_id).first()
    if not existing:
        db.session.add(Enrollment(user_id=session["user_id"], course_id=course_id))
        db.session.commit()
        flash("You are enrolled! Start learning below.", "success")
    else:
        flash("You are already enrolled in this course.", "info")
    return redirect(url_for("learn_course", course_id=course_id))

@app.route("/dashboard")
@login_required
def dashboard():
    user = db.session.get(User, session["user_id"])
    enrollments = Enrollment.query.filter_by(user_id=user.id).all()
    return render_template("dashboard.html", user=user, enrollments=enrollments)

@app.route("/learn/<int:course_id>")
@login_required
def learn_course(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        return render_template("404.html"), 404
    enrollment = Enrollment.query.filter_by(user_id=session["user_id"], course_id=course_id).first()
    if not enrollment:
        flash("Enroll in this course before viewing its lessons.", "info")
        return redirect(url_for("course_detail", slug=course.slug))
    completed = {int(x) for x in enrollment.completed_lessons.split(",") if x.strip().isdigit()}
    total = len(course.lessons)
    progress = int(len(completed) / total * 100) if total else 0
    return render_template("learn.html", course=course, enrollment=enrollment, completed=completed, progress=progress)

@app.route("/lesson/<int:lesson_id>/complete", methods=["POST"])
@login_required
def complete_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        return jsonify({"ok": False, "error": "Lesson not found"}), 404
    enrollment = Enrollment.query.filter_by(user_id=session["user_id"], course_id=lesson.course_id).first()
    if not enrollment:
        return jsonify({"ok": False, "error": "You are not enrolled"}), 403
    ids = {int(x) for x in enrollment.completed_lessons.split(",") if x.strip().isdigit()}
    ids.add(lesson_id)
    enrollment.completed_lessons = ",".join(map(str, sorted(ids)))
    db.session.commit()
    total = Lesson.query.filter_by(course_id=lesson.course_id).count()
    return jsonify({"ok": True, "completed": len(ids), "total": total, "progress": int(len(ids) / total * 100) if total else 0})

@app.route("/admin")
@admin_required
def admin():
    return render_template("admin.html", courses=Course.query.order_by(Course.id.desc()).all(),
                           users_count=User.query.count(), enrollments_count=Enrollment.query.count())

@app.route("/admin/courses/new", methods=["GET", "POST"])
@admin_required
def new_course():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip().lower().replace(" ", "-")
        category = request.form.get("category", "").strip()
        instructor = request.form.get("instructor", "").strip()
        description = request.form.get("description", "").strip()
        if not all([title, slug, category, instructor, description]):
            flash("Please complete all required fields.", "error")
            return render_template("course_form.html")
        if Course.query.filter_by(slug=slug).first():
            flash("That course URL slug is already in use.", "error")
            return render_template("course_form.html")
        course = Course(title=title, slug=slug, category=category, instructor=instructor,
                        description=description, level=request.form.get("level", "Beginner"),
                        duration=request.form.get("duration", "4 weeks"),
                        image_url=request.form.get("image_url", "").strip(),
                        featured=request.form.get("featured") == "on")
        db.session.add(course)
        db.session.flush()
        lesson_titles = [x.strip() for x in request.form.get("lessons", "").splitlines() if x.strip()]
        for i, lesson_title in enumerate(lesson_titles, 1):
            db.session.add(Lesson(course_id=course.id, title=lesson_title,
                                  summary="Work through this lesson and mark it complete when finished.",
                                  position=i))
        db.session.commit()
        flash("Course created successfully.", "success")
        return redirect(url_for("admin"))
    return render_template("course_form.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1")
