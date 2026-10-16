
https://skillsphere-q0x9.onrender.com

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
├── resume_analysis/   # Resume PDF analyzer
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

## 🚀 Free Production Deployment Guide (Render + Neon PostgreSQL)

This project is fully pre-configured for **100% FREE** production hosting with **no credit card required**:
- **Web App**: [Render](https://render.com) (Free Web Service tier, 750 free instance hours/month)
- **Database**: [Neon](https://neon.tech) (Free Serverless PostgreSQL, 500 MB storage, permanent free tier)

---

### Step 1: Create a Free PostgreSQL Database on Neon (2 minutes)

1. Sign up for free at [neon.tech](https://neon.tech) (using GitHub or Google).
2. Click **Create Project**, name it `skillsphere-db`, and choose your nearest region.
3. On the Neon dashboard, copy your **Connection String**. It looks like:
   ```text
   postgresql://neondb_owner:npg_xxxx@ep-xyz.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. Keep this connection string ready—you will use it as your `DATABASE_URL`.

---

### Step 2: (Optional) Migrate Local Data to Neon from Your PC

To transfer all quizzes, questions, and users from your local SQLite database directly to Neon:
```bash
python migrate_to_postgres.py "postgresql://neondb_owner:npg_xxxx@ep-xyz.us-east-2.aws.neon.tech/neondb?sslmode=require"
```
*(If you skip this step, Render will automatically initialize and seed the database on first deploy).*

---

### Step 3: Deploy on Render (Free Web Service)

1. Push your code to your GitHub repository.
2. Sign up / Log in to [dashboard.render.com](https://dashboard.render.com).
3. Click **New +** -> **Web Service**.
4. Select **Build and deploy from a Git repository** and connect your SkillSphere repo.
5. Fill in the following settings:
   - **Name**: `skillsphere` (or your choice)
   - **Language**: `Python`
   - **Branch**: `main` (or your active branch)
   - **Region**: Choose closest to you (e.g. Oregon or Frankfurt)
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`
   - **Instance Type**: Select **Free**
6. Under **Environment Variables**, add:

| Key | Value | Description |
|-----|-------|-------------|
| `DATABASE_URL` | `postgresql://neondb_owner:...` | Your Neon PostgreSQL connection string |
| `DJANGO_SECRET_KEY` | *(Click 'Generate' or enter a random string)* | Secret key for production |
| `DJANGO_DEBUG` | `False` | Run in production mode |
| `SERVER_TYPE` | `wsgi` (or `asgi`) | Choose `wsgi` for Gunicorn (recommended) or `asgi` for Uvicorn |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Prevents CSRF errors on forms/login |
| `DB_SSL_REQUIRE` | `True` | Enforce SSL for cloud database |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Admin username |
| `DJANGO_SUPERUSER_PASSWORD` | `YourAdminPassword123` | Admin password |

7. Click **Create Web Service**.

Render will automatically run `./build.sh` (installs packages and gathers static assets), followed by `./start.sh` (runs database migrations, seeds quizzes, sets up the superuser, and boots Gunicorn WSGI or Uvicorn ASGI).

Once deployed, visit your Render URL (e.g., `https://skillsphere.onrender.com`) to use the live app!

---

### Default Admin Credentials
- **Username**: `admin` (or whatever set in `DJANGO_SUPERUSER_USERNAME`)
- **Password**: `smbi@123` (or whatever set in `DJANGO_SUPERUSER_PASSWORD`)
- **Admin Panel URL**: `/admin/`
