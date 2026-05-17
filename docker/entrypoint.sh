#!/bin/sh
set -e

echo "마이그레이션 실행 중..."
python manage.py migrate --noinput

echo "정적 파일 수집 중..."
python manage.py collectstatic --noinput

echo "서버 시작..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3