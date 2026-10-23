# SkillSphere Seed Data Fixtures

This directory contains modularized Django JSON fixtures partitioned from `seed_data.json`.
The files are numbered with two-digit prefixes to preserve foreign-key dependencies during sequential loading.

## Fixture Files & Models

| Order | File | Models | Count | Description |
|---|---|---|---|---|
| 01 | `01_users.json` | `accounts.user` | 19 | Platform users, admin accounts, and demo student profiles |
| 02 | `02_quizzes.json` | `dashboard.quiz` | 15 | 15 curated DSA topic quizzes (Arrays, Trees, Graphs, DP, etc.) |
| 03 | `03_quiz_questions.json` | `dashboard.quizquestion` | 375 | 375 multiple-choice DSA quiz questions (25 questions per quiz) |
| 04 | `04_discussions.json` | `dashboard.discussionpost`, `dashboard.discussionreply` | 4 | Community discussion forum topics and responses |
| 05 | `05_chat_messages.json` | `dashboard.chatmessage` | 7 | Public chat room history and messages |
| 06 | `06_game_history.json` | `dashboard.gamehistory` | 1 | Speed coding and mini-game history records |
| 07 | `07_recommendations.json` | `recommendations.recommendation` | 8 | AI-powered study recommendations and roadmap items |
| 08 | `08_notifications.json` | `notifications.notification` | 19 | User activity alerts, goal notifications, and updates |
| 09 | `09_resume_analyses.json` | `resume_analysis.resumeanalysis` | 2 | ATS resume analysis sample records |
| 10 | `10_sessions.json` | `sessions.session` | 10 | Django authenticated session tokens |

## How to Load

To load all fixtures in dependency order:
```bash
python manage.py seed_db --force
```

Or manually using Django's `loaddata`:
```bash
python manage.py loaddata data/01_users.json data/02_quizzes.json data/03_quiz_questions.json data/04_discussions.json data/05_chat_messages.json data/06_game_history.json data/07_recommendations.json data/08_notifications.json data/09_resume_analyses.json data/10_sessions.json
```
