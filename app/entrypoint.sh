#!/usr/bin/env sh

mkdir /usr/src/app/database
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
