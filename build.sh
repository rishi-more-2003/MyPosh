#!/usr/bin/env bash

# set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

# Start the Gunicorn server with a custom timeout
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --timeout 120