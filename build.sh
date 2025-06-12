#!/usr/bin/env bash
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running collectstatic..."
python manage.py collectstatic --noinput --verbosity=2

echo "Build completed successfully."
