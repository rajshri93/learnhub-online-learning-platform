from app import app, db, User, Course, Lesson

SAMPLE_COURSES = [
    {
        "title": "Python for Beginners", "slug": "python-for-beginners", "category": "Programming",
        "level": "Beginner", "duration": "4 weeks", "instructor": "Aarav Kulkarni",
        "description": "Learn Python fundamentals, variables, loops, functions, and build your first small programs.",
        "featured": True, "image_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=1000&q=85",
        "lessons": ["Welcome and setup", "Variables and data types", "Conditions and loops", "Functions", "Mini project: quiz app"]
    },
    {
        "title": "Web Development Essentials", "slug": "web-development-essentials", "category": "Web Development",
        "level": "Beginner", "duration": "6 weeks", "instructor": "Meera Shah",
        "description": "Build responsive web pages with HTML, CSS, and JavaScript, then learn how the browser works.",
        "featured": True, "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1000&q=85",
        "lessons": ["How the web works", "HTML page structure", "CSS layout and responsive design", "JavaScript basics", "DOM interactions", "Project: landing page"]
    },
    {
        "title": "SQL and Database Design", "slug": "sql-database-design", "category": "Data",
        "level": "Intermediate", "duration": "3 weeks", "instructor": "Nikhil Patil",
        "description": "Understand relational databases, write SQL queries, and design clean tables with relationships.",
        "featured": True, "image_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=1000&q=85",
        "lessons": ["Tables and relationships", "SELECT and filtering", "Joins and grouping", "Keys and constraints", "Database design exercise"]
    },
    {
        "title": "UI/UX Design Foundations", "slug": "ui-ux-design-foundations", "category": "Design",
        "level": "Beginner", "duration": "2 weeks", "instructor": "Sana Merchant",
        "description": "Explore user-centered design, wireframes, visual hierarchy, and usability testing.",
        "featured": False, "image_url": "https://images.unsplash.com/photo-1558655146-9f40138edfeb?auto=format&fit=crop&w=1000&q=85",
        "lessons": ["Design thinking", "User flows", "Wireframes", "Visual hierarchy", "Usability review"]
    },
    {
        "title": "Data Structures Starter", "slug": "data-structures-starter", "category": "Computer Science",
        "level": "Intermediate", "duration": "5 weeks", "instructor": "Rohan Deshmukh",
        "description": "Build a strong foundation in arrays, stacks, queues, linked lists, and algorithmic thinking.",
        "featured": False, "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1000&q=85",
        "lessons": ["Complexity basics", "Arrays and strings", "Stacks and queues", "Linked lists", "Practice problems"]
    },
]

with app.app_context():
    db.create_all()
    for item in SAMPLE_COURSES:
        existing = Course.query.filter_by(slug=item["slug"]).first()
        if existing:
            continue
        lesson_titles = item.pop("lessons")
        course = Course(**item)
        db.session.add(course)
        db.session.flush()
        for position, title in enumerate(lesson_titles, 1):
            db.session.add(Lesson(course_id=course.id, title=title,
                                  summary=f"Learn the core ideas in {title.lower()} and try the suggested practice.",
                                  position=position))
    if not User.query.filter_by(email="admin@learnhub.local").first():
        admin = User(name="LearnHub Admin", email="admin@learnhub.local", role="admin")
        admin.set_password("ChangeMe123!")
        db.session.add(admin)
    db.session.commit()
    print("Seed complete.")
    print("Demo admin login: admin@learnhub.local / ChangeMe123!")
