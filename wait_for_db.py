#!/usr/bin/env python
"""
SkillSphere Database Readiness Check
Waits for the database to become reachable and accept queries before running migrations.
Essential for Render / Neon serverless databases during deployment wakeups.
"""
import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')

try:
    import django
    django.setup()
    from django.db import connection
    from django.db.utils import OperationalError
except Exception as err:
    print(f"Django initialization failed: {err}")
    sys.exit(1)

database_url = os.environ.get("DATABASE_URL", "").strip()
max_retries = int(os.environ.get("DB_WAIT_RETRIES", "30"))
retry_interval = int(os.environ.get("DB_WAIT_INTERVAL", "2"))

if not database_url:
    print("DATABASE_URL not set; using local SQLite database.")
    sys.exit(0)

target = database_url.split('@')[-1] if '@' in database_url else "database"
print(f"Waiting for PostgreSQL database ({target}) to become ready...")

for attempt in range(1, max_retries + 1):
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
        if row and row[0] == 1:
            print(f"Database connection successful! (Vendor: {connection.vendor})")
            sys.exit(0)
    except OperationalError as oe:
        print(f"[{attempt}/{max_retries}] Database not ready yet ({oe}). Retrying in {retry_interval}s...")
        time.sleep(retry_interval)
    except Exception as e:
        print(f"[{attempt}/{max_retries}] Waiting for database ({e}). Retrying in {retry_interval}s...")
        time.sleep(retry_interval)

print(f"ERROR: Database did not become ready after {max_retries * retry_interval} seconds.")
sys.exit(1)
