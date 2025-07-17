#!/usr/bin/env bash
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install --upgrade setuptools wheel

echo "Installing requirements..."
pip install -r requirements.txt --no-cache-dir

echo "Running collectstatic..."
python manage.py collectstatic --noinput --verbosity=2

echo "Build completed successfully."
