#! /bin/bash
sudo supervisorctl restart gunicorn
echo reloaded server
python manage.py collectstatic -l --noinput
echo reloaded static files
