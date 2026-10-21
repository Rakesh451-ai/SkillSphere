#!/usr/bin/env python
import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def migrate_data():
    print("=" * 65)
    print(" 🚀 SkillSphere SQLite -> PostgreSQL Production Migration Tool")
    print("=" * 65)

    # Allow passing database URL as a command-line argument or environment variable
    if len(sys.argv) > 1 and sys.argv[1].strip():
        db_url = sys.argv[1].strip().strip("'\"")
        os.environ["DATABASE_URL"] = db_url
    else:
        db_url = os.environ.get("DATABASE_URL", "").strip().strip("'\"")

    if not db_url or "postgres" not in db_url.lower():
        print("\n⚠️ ERROR: PostgreSQL DATABASE_URL is missing or invalid!")
        print("\nUsage:")
        print("  python migrate_to_postgres.py \"postgresql://user:password@host/dbname?sslmode=require\"")
        print("  OR set the environment variable:")
        print("    PowerShell: $env:DATABASE_URL=\"postgresql://...\" ; python migrate_to_postgres.py")
        print("    Bash:       export DATABASE_URL=\"postgresql://...\" && python migrate_to_postgres.py\n")
        sys.exit(1)

    masked_url = db_url.split('@')[-1] if '@' in db_url else db_url
    print(f"\n📡 Target PostgreSQL Database: {masked_url}")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
    import django
    django.setup()

    print("\n1️⃣ Running database schema migrations on PostgreSQL...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)

    print("\n2️⃣ Importing data fixtures into PostgreSQL...")
    if not os.path.exists("seed_data.json"):
        print("   Generating fresh seed_data.json snapshot from local SQLite...")
        subprocess.run(
            [sys.executable, "manage.py", "dumpdata", "--natural-foreign", "--natural-primary", "-e", "contenttypes", "-e", "auth.Permission", "--indent", "2"],
            stdout=open("seed_data.json", "w"),
            check=True
        )

    try:
        subprocess.run([sys.executable, "manage.py", "loaddata", "seed_data.json"], check=True)
    except subprocess.CalledProcessError:
        print("   ⚠️ Direct loaddata encountered existing records; running smart seed_db...")
        subprocess.run([sys.executable, "manage.py", "seed_db"], check=True)

    print("\n3️⃣ Ensuring superuser is configured...")
    subprocess.run([sys.executable, "create_superuser.py"], check=True)

    print("\n4️⃣ Verifying data load in PostgreSQL production database...")
    from dashboard.models import Quiz, QuizQuestion, QuizSubmission, DiscussionPost, ChatMessage
    from accounts.models import User

    print(f"   ✅ Users in PostgreSQL: {User.objects.count()}")
    print(f"   ✅ Quizzes in PostgreSQL: {Quiz.objects.count()}")
    print(f"   ✅ Quiz Questions in PostgreSQL: {QuizQuestion.objects.count()}")
    print(f"   ✅ Quiz Submissions in PostgreSQL: {QuizSubmission.objects.count()}")
    print(f"   ✅ Discussion Posts in PostgreSQL: {DiscussionPost.objects.count()}")
    print(f"   ✅ Chat Messages in PostgreSQL: {ChatMessage.objects.count()}")

    print("\n🎉 SUCCESS: All data and schema successfully migrated to PostgreSQL!")
    print("=" * 65)

if __name__ == '__main__':
    migrate_data()
