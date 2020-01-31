#!/usr/bin/env sh

mkdir /usr/src/app/database
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py parse "https://www.dropbox.com/s/1yc3rcw3nteyieb/apache_logs_1.txt?dl=1"

exec "$@"
