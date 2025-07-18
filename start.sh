#!/usr/bin/env bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --no-input

echo "Creating cache table (if using database cache)..."
python manage.py createcachetable --noinput || true

echo "Updating site domain to production domain..."
python manage.py update_site_domain

echo "Creating superuser (if needed)..."
python manage.py createsu

echo "Starting Gunicorn server..."
exec gunicorn dailyrecord.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 4 \
    --timeout 120 \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=-
