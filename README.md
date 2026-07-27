
https://skillsphere-q0x9.onrender.com

# SkillSphere 

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

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd skillsphere

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## PostgreSQL Local Setup (User-Space)

Since the development environment (such as Ubuntu Core) may restrict global package installation or root access, a self-contained, user-space PostgreSQL setup is configured for this project.

### Starting the PostgreSQL Database Server
Run the following command to start the database server:
```bash
/home/rakesh/postgresql_bin/postgresql-18.4.0-x86_64-unknown-linux-gnu/bin/pg_ctl -D /home/rakesh/postgresql_data -o "-p 5432 -k /home/rakesh/postgresql_data" -l /home/rakesh/postgresql_data/postgres.log start
```

### Stopping the PostgreSQL Database Server
Run the following command to stop the database server:
```bash
/home/rakesh/postgresql_bin/postgresql-18.4.0-x86_64-unknown-linux-gnu/bin/pg_ctl -D /home/rakesh/postgresql_data stop
```

### Accessing the Database Shell (psql)
Run the following command to connect directly to the database:
```bash
/home/rakesh/postgresql_bin/postgresql-18.4.0-x86_64-unknown-linux-gnu/bin/psql -h localhost -p 5432 -U rakesh -d skillsphere
```

## Project Structure

```
skillsphere/
├── accounts/          # Authentication & user profiles
├── dashboard/         # Analytics dashboard & charts
├── skills/            # Skill tracking system
├── studylogs/         # Daily study logger
├── goals/             # Goal management
├── recommendations/   # AI recommendation engine
├── resumeanalyzer/    # Resume PDF analyzer
├── leaderboard/       # Rankings & gamification
├── notifications/     # Notification system
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploads
├── skillsphere/       # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── api_urls.py
│   └── api_views.py
├── manage.py
└── requirements.txt
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/skills/` | GET, POST | List/create skills |
| `/api/studylogs/` | GET, POST | List/create study logs |
| `/api/goals/` | GET, POST | List/create goals |
| `/api/recommendations/` | GET | List recommendations |
| `/api/profile/` | GET, PUT | View/update profile |

## Deployment

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Secret key for Django | Auto-generated |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `*` |

This whole project is made using AI

### Production (Render/Railway)

1. Set environment variables
2. Use PostgreSQL database
3. Run `python manage.py collectstatic`
4. Use Gunicorn: `gunicorn skillsphere.wsgi`
