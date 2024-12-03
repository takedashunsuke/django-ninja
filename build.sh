#!/bin/bash
# Set the Django settings module to staging
# export DJANGO_SETTINGS_MODULE=config.settings.staging

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (optional, only if needed for production)
python manage.py collectstatic --settings config.settings.staging --noinput

# Apply database migrations
python manage.py migrate --settings config.settings.staging

# python manage.py createsuperuser
