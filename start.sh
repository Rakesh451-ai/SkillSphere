#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=================================================="
echo "🚀 SkillSphere Web Service Starting"
echo "=================================================="

# Check and wait for database connection readiness
echo "⏳ Checking database connection readiness..."
python wait_for_db.py

# Apply database migrations
echo "🔄 Applying database migrations..."
python manage.py migrate --noinput

# Seed default data if database is fresh
echo "🌱 Checking and seeding initial platform data..."
python manage.py seed_db

# Configure default superuser
echo "👤 Ensuring superuser is configured..."
python create_superuser.py

# Determine port (Render and Railway set $PORT automatically)
PORT="${PORT:-8000}"

# Determine gateway type: 'wsgi' (recommended default) or 'asgi'
SERVER_TYPE="${SERVER_TYPE:-wsgi}"

if [ "$SERVER_TYPE" = "asgi" ]; then
    echo "⚡ Starting ASGI server (Uvicorn) on 0.0.0.0:$PORT..."
    exec uvicorn skillsphere.asgi:application \
        --host 0.0.0.0 \
        --port "$PORT" \
        --workers 2 \
        --timeout-keep-alive 120
else
    echo "🌐 Starting WSGI server (Gunicorn) on 0.0.0.0:$PORT..."
    exec gunicorn skillsphere.wsgi:application \
        --bind 0.0.0.0:"$PORT" \
        --workers 2 \
        --threads 4 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
fi
