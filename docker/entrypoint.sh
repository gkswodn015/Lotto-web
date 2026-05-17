#!/bin/sh
set -e

echo 'Waiting for DB...'
sleep 5

echo 'Running migrate...'
python manage.py migrate --noinput

echo 'Collecting static...'
python manage.py collectstatic --noinput

echo 'Starting server...'
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
