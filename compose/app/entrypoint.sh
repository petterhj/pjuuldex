#!/bin/bash

echo "Migrating database..."

python manage.py makemigrations pokedex
python manage.py migrate --noinput

echo "Collecting statc files, target ${DJANGO_STATIC_ROOT}"

cp -r /app/tmp/* /app/dist
rm -r /app/tmp/

python manage.py collectstatic --noinput

/usr/local/bin/gunicorn wsgi --bind 0.0.0.0:8000 --chdir=/app/src
