#! /bin/bash

while getopts ":s" opt; do
  case $opt in
    s)
      echo "reloading static files"
      python manage.py collectstatic --noinput
      echo "reloaded static files"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

echo "reloading server"
sudo supervisorctl restart gunicorn
echo "reloaded server"
