
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

## 🚀 Complete Production Deployment on Render with Working Database

SkillSphere is fully configured to deploy on **Render** with a **working PostgreSQL database**. You can deploy using either of two methods:

---

### Option A: 1-Click Render Blueprint (Recommended — 100% Automated)

Render Blueprints use [`render.yaml`](render.yaml) to automatically provision both the **Web Service** and the **PostgreSQL Database** in one go, without copying any database credentials.

1. Push your latest code to your GitHub repository:
   ```bash
   git push origin <your-active-branch>
   ```
2. Log in to [dashboard.render.com](https://dashboard.render.com).
3. Click **New +** (top right) -> **Blueprint**.
4. Connect your **SkillSphere** GitHub repository.
5. Choose your active branch (`skillsphere-complete` or `main`).
6. Render will detect [`render.yaml`](render.yaml) and automatically create:
   - **Database**: `skillsphere-db` (Free PostgreSQL instance)
   - **Web Service**: `skillsphere` (Python Web Service)
   - Auto-wires `DATABASE_URL` directly from `skillsphere-db` to the web app.
7. Click **Apply**.
8. Render will run `bash build.sh` followed by `bash start.sh`:
   - Dependencies are installed.
   - Static files are compressed & collected.
   - `wait_for_db.py` confirms database availability.
   - Database migrations are automatically applied.
   - Initial platform data (15 DSA quizzes, 375 questions) is auto-seeded.
   - The default superuser is configured.
   - Gunicorn starts serving your app!

---

### Option B: Manual Web Service Setup (Render PostgreSQL or Neon.tech)

If you prefer configuring services manually or using a permanent free external PostgreSQL database like [Neon.tech](https://neon.tech):

#### Step 1: Create a PostgreSQL Database
- **Option 1 (Render Native PostgreSQL)**:
  1. In Render dashboard, click **New +** -> **PostgreSQL**.
  2. Set Name to `skillsphere-db`, Region to **Oregon** (or your preferred region), and choose the **Free** plan.
  3. Click **Create Database**.
  4. Once created, copy the **Internal Database URL** (e.g. `postgres://skillsphere_db_user:...@dpg-xxxx-a:5432/skillsphere_db`).
- **Option 2 (Neon Serverless PostgreSQL — Permanent Free Tier)**:
  1. Sign up at [neon.tech](https://neon.tech) and create a project `skillsphere-db`.
  2. Copy the **Connection String** with `?sslmode=require`.

#### Step 2: Create the Web Service on Render
1. In Render dashboard, click **New +** -> **Web Service**.
2. Connect your **SkillSphere** repository.
3. Configure the following settings:
   - **Name**: `skillsphere`
   - **Runtime**: `Python`
   - **Branch**: `skillsphere-complete` (or `main`)
   - **Region**: Same region as your database
   - **Build Command**: `bash build.sh`
   - **Start Command**: `bash start.sh`
   - **Plan**: `Free`

4. In **Environment Variables**, add:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | *(Paste Internal DB URL from Render or Neon URL)* | Working PostgreSQL database connection string |
| `DJANGO_SECRET_KEY` | *(Click 'Generate' or enter a random string)* | Production secret key |
| `DJANGO_DEBUG` | `False` | Production mode |
| `SERVER_TYPE` | `wsgi` | High-performance Gunicorn WSGI server |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Prevents CSRF forbidden errors |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Admin username |
| `DJANGO_SUPERUSER_EMAIL` | `admin@skillsphere.app` | Admin email |
| `DJANGO_SUPERUSER_PASSWORD` | `admin12345` | Admin password |

5. Click **Create Web Service**.

---

### Verifying the Live Deployment

Once the deployment finishes:
1. Open your live Render URL (e.g. `https://skillsphere.onrender.com`).
2. Log in at `/accounts/login/` or access the Admin Panel at `/admin/`.
3. Default credentials:
   - **Username**: `admin`
   - **Password**: `admin12345` (or whatever set in `DJANGO_SUPERUSER_PASSWORD`)
4. Verify that:
   - All 15 DSA Quizzes & 375 Questions are available.
   - User registration and login work seamlessly.
   - Data persists across server restarts in the PostgreSQL database.

---

### (Optional) Local to PostgreSQL Migration Tool

If you ever want to push your local SQLite data directly to any PostgreSQL database from your terminal:
```bash
python migrate_to_postgres.py "postgresql://user:password@host/dbname?sslmode=require"
```
