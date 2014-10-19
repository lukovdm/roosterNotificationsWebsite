#! /bin/bash
gunicorn --reload roosterNotificationsWebsite.wsgi:application
echo reloaded
