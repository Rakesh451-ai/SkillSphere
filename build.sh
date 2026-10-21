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

echo "✨ Build completed successfully!"
