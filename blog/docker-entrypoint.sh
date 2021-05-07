#!/bin/sh
if ["$DATABASE" = "postgres"]
then
    echo "Waiting for $DATABASE..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "Postgresql started successfully!"
fi

# flush the previous db tables
python manage.py flush --no-input
# apply new migrations
python manage.py migrate
# create a superuser to manage the new posts
python manage.py createsuperuser --no-input
# load fake data into project to
python fake-import.py

exec "$@"