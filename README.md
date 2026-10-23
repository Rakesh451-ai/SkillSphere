
# SkillSphere – AI Powered Student Growth Tracker

A complete startup-style Django platform for students to track skills, productivity, placement preparation, and growth analytics.

## Features

- **Authentication System** — Registration, login/logout, profile management with college/branch/year details
- **Student Dashboard** — Analytics cards, weekly study charts, skill progress, productivity graphs, and monthly analytics
- **Skill Tracking** — Track skills across categories (DSA, Web Dev, Communication, Aptitude, AI/ML, Core Subjects) with levels (Beginner/Intermediate/Advanced)
- **Daily Study Logger** — Log study sessions with topics, hours, productivity ratings, and notes
- **AI Recommendation System** — Rule-based engine that analyzes activity and generates personalized suggestions
- **Placement Readiness Analyzer** — Score calculated from skills, consistency, goals, resume quality, and study hours
- **Resume Analyzer** — Upload PDF resumes for instant analysis with scoring, section detection, and improvement suggestions
- **Goal Management** — Create daily/weekly/monthly goals with progress tracking
- **Leaderboard & Gamification** — XP points, streaks, badges, achievements, and student rankings
- **Notifications** — Goal reminders, study reminders, achievement notifications
- **REST API** — Full API for all modules using Django REST Framework
- **Admin Panel** — Customized admin interface for managing users, analytics, and platform data

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts**: Chart.js
- **AI/ML**: Rule-based recommendation engine (Pandas, NumPy, scikit-learn available)
- **Database**: SQLite (development), PostgreSQL (production)

## Quick Start (Local Development)

```bash
# Clone the repository
git clone https://github.com/Rakesh451-ai/SkillSphere.git
cd SkillSphere

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed database with initial quizzes & questions
python manage.py seed_db

# Create superuser
python create_superuser.py

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.


python migrate_to_postgres.py "postgresql://user:password@host/dbname?sslmode=require"
```
