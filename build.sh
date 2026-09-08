#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email admin@gitapath.com || true
python seed_data.py