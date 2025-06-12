#!/usr/bin/env bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --no-input

echo "Creating superuser (if needed)..."
python manage.py createsuperuser \
    --no-input \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" \
    --first_name "$DJANGO_SUPERUSER_FIRST_NAME" \
    --last_name "$DJANGO_SUPERUSER_LAST_NAME" || true

echo "Starting Gunicorn server..."
exec gunicorn dailyrecord.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 4 \
    --timeout 120 \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=-
