#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip

pip install -r requirements.txt
echo "Collect static files"
python manage.py collectstatic 
# check if static files are collected
ls -l ./staticfiles
echo "Apply database migrations"
python manage.py migrate
