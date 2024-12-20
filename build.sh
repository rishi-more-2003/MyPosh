# !/usr/bin/env bash

# set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

gunicorn -w 2 -b 0.0.0.0:10000 backend.wsgi:application --timeout 120 