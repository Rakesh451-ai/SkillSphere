#!/usr/bin/env python
import os
import sys
import subprocess
import django

def migrate_data():
    print("=" * 65)
    print(" 🚀 SkillSphere SQLite -> PostgreSQL Production Migration Tool")
    print("=" * 65)

    db_url = os.environ.get("DATABASE_URL", "").strip().strip("'\"")

    if not db_url or "postgres" not in db_url.lower():
        print("\n⚠️ ERROR: DATABASE_URL environment variable is missing or not a PostgreSQL URL!")
        print("Please set your PostgreSQL connection string, for example:")
        print("export DATABASE_URL='postgresql://user:password@host:5432/dbname'\n")
        sys.exit(1)

    print(f"\n📡 Connecting to PostgreSQL database at: {db_url.split('@')[-1] if '@' in db_url else db_url}")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
    django.setup()

    print("\n1️⃣ Running database schema migrations on PostgreSQL...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)

    print("\n2️⃣ Importing all SQLite data fixture (seed_data.json) into PostgreSQL...")
    if not os.path.exists("seed_data.json"):
        print("   Generating fresh seed_data.json snapshot from local SQLite...")
        subprocess.run([sys.executable, "manage.py", "dumpdata", "--natural-foreign", "--natural-primary", "-e", "contenttypes", "-e", "auth.Permission", "--indent", "2"], stdout=open("seed_data.json", "w"), check=True)

    subprocess.run([sys.executable, "manage.py", "loaddata", "seed_data.json"], check=True)

    print("\n3️⃣ Verifying data load in PostgreSQL production database...")
    from dashboard.models import Quiz, QuizQuestion, QuizSubmission, DiscussionPost, ChatMessage
    from accounts.models import User

    print(f"   ✅ Users in PostgreSQL: {User.objects.count()}")
    print(f"   ✅ Quizzes in PostgreSQL: {Quiz.objects.count()}")
    print(f"   ✅ Quiz Questions in PostgreSQL: {QuizQuestion.objects.count()}")
    print(f"   ✅ Quiz Submissions in PostgreSQL: {QuizSubmission.objects.count()}")
    print(f"   ✅ Discussion Posts in PostgreSQL: {DiscussionPost.objects.count()}")
    print(f"   ✅ Chat Messages in PostgreSQL: {ChatMessage.objects.count()}")

    print("\n🎉 SUCCESS: All SQLite data successfully copied & loaded into PostgreSQL!")
    print("=" * 65)

if __name__ == '__main__':
    migrate_data()
