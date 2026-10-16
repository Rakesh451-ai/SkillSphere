#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=================================================="
echo "📦 SkillSphere Build Process"
echo "=================================================="

echo "⬇️ Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

if [ -n "$DATABASE_URL" ]; then
    echo "🔄 DATABASE_URL found. Applying database migrations..."
    python manage.py migrate --noinput || echo "⚠️ Build-time migration skipped (will run on startup)."
fi

echo "✨ Build completed successfully!"