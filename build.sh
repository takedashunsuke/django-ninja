#!/bin/bash
# Set the Django settings module to staging
# export DJANGO_SETTINGS_MODULE=config.settings.staging

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (optional, only if needed for production)
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# python manage.py createsuperuser
