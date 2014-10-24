#! /bin/bash
gunicorn --reload roosterNotificationsWebsite.wsgi:application
echo reloaded server
python manage.py collectstatic -l
echo reloaded static files
