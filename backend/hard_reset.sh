#!/bin/bash
dropdb -U postgres -f "${DATABASE}"
createdb -U postgres "${DATABASE}"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput
python manage.py createcachetable